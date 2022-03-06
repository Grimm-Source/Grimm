from datetime import datetime, timedelta

from grimm import logger, db
from grimm.models.activity import ActivityParticipant, PickupImpaired, Activity, PickupVolunteer
from grimm.models.admin import User
from grimm.utils import misctools, constants, smstools


def activity_converter(activity, openid=0):
    query = {}
    logger.info('Convert activity dto.')
    query["id"] = activity["id"]
    query["adminId"] = activity["approver"]
    query["title"] = activity["title"]
    query["location"] = activity["location"]
    query["sign_in_radius"] = activity["sign_in_radius"]
    query["sign_in_token"] = activity["sign_in_token"]
    query["start_time"] = activity["start_time"].strftime("%Y-%m-%dT%H:%M:%S")
    query["end_time"] = activity["end_time"].strftime("%Y-%m-%dT%H:%M:%S")
    query["duration"] = misctools.calc_duration(activity["start_time"], activity["end_time"])
    query["content"] = activity["content"]
    query["notice"] = activity["notice"]
    query["others"] = activity["others"]
    query["tag"] = ','.join([constants.TAG_LIST[int(tid)] for tid in activity["tag_ids"].split(',') if tid or int(tid) in range(6)]) \
        if activity["tag_ids"] else ''
    if openid == 0:
        participant = ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity["id"]).all()
        query["share"] = sum([int(part.share) for part in participant])
    else:
        participant = ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity["id"],
                                                       ActivityParticipant.participant_openid == openid).first()
        query["share"] = int(participant.share)
    query["interested"] = ActivityParticipant.query. \
        filter(ActivityParticipant.activity_id == activity["id"],
               ActivityParticipant.interested == 1).count() if openid == 0 \
        else ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity["id"],
                                              ActivityParticipant.participant_openid == openid,
                                              ActivityParticipant.interested == 1).count()
    query["thumbs_up"] = ActivityParticipant.query. \
        filter(ActivityParticipant.activity_id == activity["id"],
               ActivityParticipant.thumbs_up == 1).count()
    query["registered"] = ActivityParticipant.query. \
        filter(ActivityParticipant.activity_id == activity["id"],
               ActivityParticipant.current_state == 'Registered').count() if openid == 0 else \
        ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity["id"],
                                         ActivityParticipant.participant_openid == openid,
                                         ActivityParticipant.current_state == 'Registered').count()
    query["registered_volunteer"] = db.session.query(ActivityParticipant, User). \
        filter(ActivityParticipant.activity_id == activity["id"],
               ActivityParticipant.current_state == 'Registered'). \
        filter(User.role == 0). \
        filter(ActivityParticipant.participant_openid == User.openid).count()
    query["registered_impaired"] = db.session.query(ActivityParticipant, User). \
        filter(ActivityParticipant.activity_id == activity["id"],
               ActivityParticipant.current_state == 'Registered'). \
        filter(User.role == 1). \
        filter(ActivityParticipant.participant_openid == User.openid).count()
    query["volunteer_capacity"] = activity["volunteer_capacity"]
    query["is_volunteer_limited"] = (
        True
        if (
                activity["volunteer_capacity"] is not None
                and activity["volunteer_capacity"] > 0
        )
        else False
    )
    query["vision_impaired_capacity"] = activity["vision_impaired_capacity"]
    query["is_impaired_limited"] = (
        True
        if (
                activity["vision_impaired_capacity"] is not None
                and activity["vision_impaired_capacity"] > 0
        )
        else False
    )
    query["volunteer_job_title"] = activity["volunteer_job_title"]
    query["volunteer_job_content"] = activity["volunteer_job_content"]
    query["activity_fee"] = activity["activity_fee"]
    query["is_fee_needed"] = (
        True
        if (activity["activity_fee"] is not None and activity["activity_fee"] > 0)
        else False
    )
    query["activity_them_pic_name"] = activity['theme_pic_name']
    return query


def sort_by_time(activities_info, filter_time):
    if filter_time == "all":
        return reversed(
            [
                activity
                for activity in activities_info
                if datetime.today() - timedelta(days=365) < activity["end_time"]
            ]
        )
    elif filter_time == "latest":
        return reversed(
            [
                activity
                for activity in activities_info
                if datetime.today() < activity["end_time"]
            ]
        )
    elif filter_time == "weekends":
        res_info = [
            activity
            for activity in activities_info
            if should_append_by_weekends(activity)
        ]
        return sorted(res_info, key=lambda activity: activity["start_time"])
    elif filter_time == "recents":
        res_info = [
            activity
            for activity in activities_info
            if should_append_by_recents(activity)
        ]
        return sorted(res_info, key=lambda activity: activity["start_time"])
    else:
        res_info = [
            activity
            for activity in activities_info
            if should_append_by_time_span(activity, filter_time)
        ]
        return sorted(res_info, key=lambda activity: activity["start_time"])


def should_append_by_time_span(activity, filter_time):
    filter_start = datetime.strptime(filter_time.split(" - ")[0], "%Y-%m-%d")
    filter_end = datetime.strptime(filter_time.split(" - ")[1], "%Y-%m-%d") + timedelta(days=1)
    start = activity["start_time"]
    end = activity["end_time"]
    if filter_end < start or filter_start > end:
        return False
    return True


def should_append_by_tag(activity, target_tag_list):
    if not activity:
        return False
    if target_tag_list == "all":
        return True
    if activity["tag_ids"] is not None:
        current_tag_list = activity["tag_ids"].split(",")
        for target_tag_id in target_tag_list.split(","):
            if target_tag_id in current_tag_list:
                return True
    return False


def should_append_by_weekends(activity):
    today = datetime.today()
    end = activity["end_time"]
    if today > end:
        return False
    start = activity["start_time"] if activity["start_time"] > today else today
    while start < end:
        if start.weekday() >= 5:
            return True
        start += timedelta(days=1)
    return False


def should_append_by_recents(activity):
    filter_start = datetime.today()
    filter_end = filter_start + timedelta(days=7)
    start = activity["start_time"]
    end = activity["end_time"]
    if filter_end < start or filter_start > end:
        return False
    return True


def user_cancel_activity(openid, activity_id):
    """ Volunteer cancel participation from wechat-end, should notice impaired or volunteer asap."""
    user_info = User.query.filter(User.openid == openid).first()
    activity_info = Activity.query.filter(Activity.id == activity_id).first()
    logger.info('User %s cancel activity %s, should remove the '
                'binding and give some notifications.' % (user_info.name, activity_info.title))
    if user_info.role == 0:
        logger.info('volunteer %s cancel activity %s.' % (user_info.name, activity_info.title))
        pick_info = db.session.query(PickupVolunteer).\
            filter(PickupVolunteer.openid == openid,
                   PickupVolunteer.activity_id == activity_id).first()
        if pick_info:
            logger.info('Query pickup list for volunteer %s' % user_info.name)
            pick_list = PickupImpaired.query. \
                filter(PickupImpaired.pickup_volunteer_openid == openid,
                       PickupImpaired.activity_id == activity_id).all()
            if pick_list:
                for pick in pick_list:
                    impaired_openid = pick.openid
                    pick_impaired = db.session.query(PickupImpaired). \
                        filter(PickupImpaired.activity_id == activity_id,
                               PickupImpaired.openid == impaired_openid).first()
                    logger.info('Clear pickup info and notice impaired %s' % pick_impaired.name)
                    pick_impaired.pick_method = ''
                    pick_impaired.pickup_volunteer_openid = ''
                    db.session.commit()
                    kwargs = {
                        'impaired_name': pick_impaired.name,
                        'volunteer_name': pick_info.name,
                        'volunteer_phone': user_info.phone
                    }
                    impaired_user_info = User.query.filter(User.openid == impaired_openid).first()
                    phone_number_list = [impaired_user_info.phone]
                    template_id = constants.TEMPLATE_CODES['VOLUNTEER_CANCEL_ACTIVITY']
                    smstools.send_short_message(phone_number_list, template_id, **kwargs)
                logger.info('all impaired notice over.')
            db.session.delete(pick_info)
            db.session.commit()
    else:
        logger.info('Impaired %s cancel activity %s.' % (user_info.name, activity_info.title))
        pickup_impaired = db.session.query(PickupImpaired). \
            filter(PickupImpaired.openid == openid,
                   PickupImpaired.activity_id == activity_id).first()
        if pickup_impaired:
            logger.info('Have volunteer pickup current impaired? if yes, need notice volunteer.')
            if pickup_impaired.pickup_volunteer_openid and pickup_impaired.pickup_method:
                volunteer_user_info = User.query.filter(User.openid == pickup_impaired.pickup_volunteer_openid).first()
                logger.info("Current impaired volunteer is %s" % volunteer_user_info.name)
                kwargs = {
                    'impaired_name': pickup_impaired.name,
                    'volunteer_name': volunteer_user_info.name,
                    'impaired_phone': user_info.phone
                }
                phone_number_list = [volunteer_user_info.phone]
                template_id = constants.TEMPLATE_CODES['IMPAIRED_CANCEL_ACTIVITY']
                smstools.send_short_message(phone_number_list, template_id, **kwargs)
            db.session.delete(pickup_impaired)
            db.session.commit()
    logger.info('Volunteer or impaired %s cancel activity success.' % user_info.name)


def volunteer_pickup_impaired(volunteer_openid, impaired_openid, pickup_method):
    """ volunteer choose pickup impaired and detail pickup method """
    logger.info('Volunteer choose pickup method. need to notice impaired.')
    volunteer_user_info = User.query.filter(User.openid == volunteer_openid).first()
    impaired_user_info = User.query.filter(User.openid == impaired_openid).first()
    kwargs = {'impaired_name': impaired_user_info.name,
              'volunteer_name': volunteer_user_info.name,
              'volunteer_phone': volunteer_user_info.phone}
    phone_number_list = [impaired_user_info.phone]
    if pickup_method:
        logger.info('Volunteer %s will pickup %s' % (volunteer_user_info.name, impaired_user_info.name))
        template_id = constants.TEMPLATE_CODES['VOLUNTEER_PICKUP']
        smstools.send_short_message(phone_number_list, template_id, **kwargs)
    else:
        logger.info('Volunteer %s not pickup %s' % (volunteer_user_info.name, impaired_user_info.name))
        template_id = constants.TEMPLATE_CODES['VOLUNTEER_CANCEL_PICKUP']
        smstools.send_short_message(phone_number_list, template_id, **kwargs)
