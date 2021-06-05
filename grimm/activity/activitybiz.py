from datetime import datetime, timedelta

from grimm import logger, db
from grimm.models.activity import ActivityParticipant
from grimm.models.admin import User
from grimm.utils import misctools, constants


def activity_converter(activity, openid=0):
    query = {}
    logger.info('Convert activity dto.')
    query["id"] = activity["id"]
    query["adminId"] = activity["approver"]
    query["title"] = activity["title"]
    query["location"] = activity["location"]
    query["sign_in_radius"] = activity["sign_in_radius"]
    query["start_time"] = activity["start_time"].strftime("%Y-%m-%dT%H:%M:%S")
    query["end_time"] = activity["end_time"].strftime("%Y-%m-%dT%H:%M:%S")
    query["duration"] = misctools.calc_duration(activity["start_time"], activity["end_time"])
    query["content"] = activity["content"]
    query["notice"] = activity["notice"]
    query["others"] = activity["others"]
    query["tag"] = ','.join([constants.TAG_LIST[int(tid)] for tid in activity["tag_ids"].split(',') if tid or int(tid) in range(6)]) \
        if activity["tag_ids"] else ''
    query["share"] = ActivityParticipant.query. \
        filter(ActivityParticipant.activity_id == activity["id"],
               ActivityParticipant.share == 1).count()
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
        filter(ActivityParticipant.activity_id == activity["id"]).count() if openid == 0 else \
        ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity["id"],
                                         ActivityParticipant.participant_openid == openid).count()
    query["registered_volunteer"] = db.session.query(ActivityParticipant, User). \
        filter(ActivityParticipant.activity_id == activity["id"]). \
        filter(User.role == 0). \
        filter(ActivityParticipant.participant_openid == User.openid).count()
    query["registered_impaired"] = db.session.query(ActivityParticipant, User). \
        filter(ActivityParticipant.activity_id == activity["id"]). \
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
