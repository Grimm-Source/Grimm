import json
import os
import uuid
from datetime import datetime, timedelta
from urllib.parse import unquote_plus

from flask import request, jsonify, send_file
from flask_restx import Resource, reqparse
from six.moves.urllib.parse import quote

from config import BASE_DIR
from grimm import logger, db
from grimm.activity import activity, activitybiz
from grimm.models.activity import Activity, ActivityParticipant, PickupVolunteer, PickupImpaired
from grimm.models.activity import Project, Duty, Gift
from grimm.models.admin import User
from grimm.utils import dbutils, certificationgenerate, emailverify, areautils
from grimm.utils.constants import TAG_LIST


@activity.route("/activities", methods=['GET'])
class Activities(Resource):
    def get(self):
        keyword = request.args.get("keyword")
        activities_info = Activity.query.all()
        activities_info = [dbutils.serialize(rep) for rep in activities_info]
        if not activities_info:
            return jsonify([])

        if keyword and len(keyword) != 0:
            queries = [activitybiz.activity_converter(activity)
                       for activity in activities_info if activity and keyword in activity["title"]]
            logger.info("get all activities successfully")
            return jsonify(queries)

        target_tag_list = request.args.get("tags")
        if not target_tag_list or len(target_tag_list) == 0:
            target_tag_list = "all"
        filter_time = request.args.get("time")
        if not filter_time or len(filter_time) == 0:
            filter_time = "all"
        sorted_activities_info = activitybiz.sort_by_time(activities_info, filter_time)
        queries = [activitybiz.activity_converter(activity)
                   for activity in sorted_activities_info
                   if activitybiz.should_append_by_tag(activity, target_tag_list)]
        logger.info("get all activities successfully")
        return jsonify(queries)


@activity.route("/activity", methods=["POST"])
class NewActivity(Resource):
    def post(self):
        """ view function to add new activity """
        info = json.loads(request.get_data())
        activity_info = Activity()
        logger.info('Add activity.')
        activity_info.approver = info["adminId"]
        activity_info.title = info["title"]
        activity_info.location = info["location"]
        status, lat_lng = areautils.address_to_coordinate(info["location"])
        if status:
            activity_info.location_latitude = lat_lng['lat']
            activity_info.location_longitude = lat_lng['lng']
        else:
            return jsonify({"status": "failure"})
        # activity_info.location_latitude = info["location_latitude"]
        # activity_info.location_longitude = info["location_longitude"]
        activity_info.sign_in_radius = info["sign_in_radius"]
        activity_info.sign_in_token = info["sign_in_token"]
        if len(info['activity_them_pic_name']) == 0 \
                or 'url' not in info['activity_them_pic_name'][0] \
                or not info['activity_them_pic_name'][0]['url']:
            logger.warning("Add activity failed, no theme picture.")
            feedback = {"status": "failure", "message": "请上传活动主题图片"}
            return jsonify(feedback)
        activity_info.theme_pic_name = quote(info['activity_them_pic_name'][0]['url'])
        activity_info.start_time = info["start_time"]
        activity_info.end_time = info["end_time"]
        activity_info.content = info["content"]
        activity_info.notice = info["notice"]
        activity_info.others = info["others"]
        activity_info.admin_raiser = info["adminId"]
        ids = ','.join([str(TAG_LIST.index(t)) for t in info["tag"].split(',') if t and t in TAG_LIST]) if info["tag"] else ''
        activity_info.tag_ids = ids
        activity_info.volunteer_capacity = info["volunteer_capacity"]
        activity_info.vision_impaired_capacity = info["vision_impaired_capacity"]
        activity_info.volunteer_job_title = info["volunteer_job_title"]
        activity_info.volunteer_job_content = info["volunteer_job_content"]
        activity_info.activity_fee = info["activity_fee"] if 'activity_fee' in info else 0
        db.session.add(activity_info)
        db.session.commit()
        logger.info("%s: create new activity successfully", activity_info.title)
        return jsonify({"status": "success"})


@activity.route("/activity/<int:activity_id>", methods=["POST", "GET", "DELETE"])
class ActivityOperate(Resource):
    def get(self, activity_id):
        activity_info = Activity.query.filter(Activity.id == activity_id).first()
        if not activity_info:
            logger.warning("%d: no such activity", activity_id)
            return jsonify({"status": "failure", "message": "未知活动ID"})
        file_name = activity_info.theme_pic_name
        feedback = activitybiz.activity_converter(dbutils.serialize(activity_info))
        feedback['activity_them_pic_name'] = file_name
        logger.info("%d: get activity successfully", activity_id)
        return jsonify(feedback)

    def post(self, activity_id):
        new_info = json.loads(request.get_data())
        activity_info = db.session.query(Activity).filter(Activity.id == activity_id).first()
        if not activity_info:
            logger.warning("%d: update activity failed", activity_id)
            feedback = {"status": "failure", "message": "无效活动 ID"}
            return jsonify(feedback)
        if len(new_info['activity_them_pic_name']) == 0:
            logger.warning("%d: update activity failed, no theme picture.", activity_id)
            feedback = {"status": "failure", "message": "请上传活动主题图片"}
            return jsonify(feedback)
        logger.info('Will update activity.')
        activity_info.theme_pic_name = new_info['activity_them_pic_name'][0]['url']
        activity_info.approver = new_info["adminId"]
        activity_info.title = new_info["title"]
        activity_info.location = new_info["location"]
        status, lat_lng = areautils.address_to_coordinate(new_info["location"])
        if status:
            activity_info.location_latitude = lat_lng['lat']
            activity_info.location_longitude = lat_lng['lng']
        else:
            jsonify({"status": "failure"})
        # activity_info.location_latitude = new_info["location_latitude"]
        # activity_info.location_longitude = new_info["location_longitude"]
        activity_info.sign_in_radius = new_info["sign_in_radius"]
        activity_info.sign_in_token = new_info["sign_in_token"]
        activity_info.start_time = new_info["start_time"]
        activity_info.end_time = new_info["end_time"]
        activity_info.content = new_info["content"]
        activity_info.notice = new_info["notice"]
        activity_info.others = new_info["others"]
        activity_info.admin_raiser = new_info["adminId"]
        ids = ','.join([str(TAG_LIST.index(t)) for t in new_info["tag"].split(',') if t and t in TAG_LIST]) if new_info["tag"] else ''
        activity_info.tag_ids = ids
        activity_info.volunteer_capacity = new_info["volunteer_capacity"]
        activity_info.vision_impaired_capacity = new_info["vision_impaired_capacity"]
        activity_info.volunteer_job_title = new_info["volunteer_job_title"]
        activity_info.volunteer_job_content = new_info["volunteer_job_content"]
        activity_info.activity_fee = new_info["activity_fee"]
        db.session.commit()
        logger.info("%d: update activity successfully", activity_id)
        return jsonify({"status": "success"})

    def delete(self, activity_id):
        participants = ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity_id).first()
        if participants:
            return jsonify({"status": "failure", "message": "已有用户操作过该活动，不能删除！"})
        activity_info = Activity.query.filter(Activity.id == activity_id).first()
        db.session.delete(activity_info)
        db.session.commit()
        logger.info("%d: delete new activity successfully", activity_id)
        return jsonify({"status": "success", "message": "活动删除成功！"})


@activity.route("/activity/themePic", methods=["POST", "GET"])
class ActivityThemePic(Resource):
    def get(self):
        activity_id = request.args.get('activity_id')
        if activity_id:
            activity_info = Activity.query.filter(Activity.id == activity_id).first()
            if activity_info is None:
                return jsonify({'status': 'failure', 'message': 'Activity not exists.'})

            filename = activity_info.theme_pic_name
        else:
            filename = request.args.get('activity_them_pic_name')
        if not filename:
            return jsonify({'status': 'failure', 'message': 'Please input activity id or file name.'})
        image = os.path.join(BASE_DIR, 'static/activity_theme_pictures/' + unquote_plus(filename))
        return send_file(image)

    def post(self):
        file_storage = request.files.get('activity_them_pic_name')
        if not file_storage:
            return jsonify({"status": 0, "message": 'No file found'})
        pic_id = str(uuid.uuid4()).replace('-', '') + datetime.now().strftime('%Y%m%d%H%M%S')
        new_file_name = pic_id + '-' + file_storage.filename
        new_file_path = os.path.join(BASE_DIR, "static/activity_theme_pictures/" + new_file_name)
        file_storage.save(new_file_path)
        return jsonify({"status": 1, "fileName": new_file_name})


@activity.route("/activityRegistration/<int:activity_id>", methods=["POST", "GET"])
class ActivityRegistration(Resource):
    def get(self, activity_id):
        activity_info = Activity.query.filter(Activity.id == activity_id).first()
        if not activity_info:
            logger.warning("%d: no such activity", activity_id)
            return jsonify({"status": "failure", "message": "无效活动 ID"})
        activities_registration = ActivityParticipant.query.filter(ActivityParticipant.activity_id == activity_id).all()
        users = []
        for item in activities_registration:
            user = {}
            openid = item.participant_openid
            user_info = User.query.filter(User.openid == openid).first()
            user["openid"] = openid
            user["name"] = user_info.name
            user["role"] = user_info.role
            user["phone"] = user_info.phone
            user["address"] = user_info.address

            user["needpickup"] = 0
            user["topickup"] = 0

            role = user_info.role
            if role == 0:   # volunteer
                pickup_volunteer = PickupVolunteer.query\
                    .filter(PickupVolunteer.openid == openid,
                            PickupVolunteer.activity_id == activity_id).first()
                if pickup_volunteer:
                    user["topickup"] = 1
            else:  # impaired
                pickup_impaired = PickupImpaired.query\
                    .filter(PickupImpaired.openid == openid,
                            PickupImpaired.activity_id == activity_id).first()
                if pickup_impaired:
                    user["needpickup"] = 1
            # user["accepted"] = item.accepted
            # user["needpickup"] = item.needpickup
            # user["topickup"] = item.topickup
            user['current_state'] = item.current_state if item.current_state is not None else 'canceled'
            users.append(user)
        feedback = {'status': 'success', 'users': users}
        return jsonify(feedback)

    def post(self, activity_id):
        activity_info = Activity.query.filter(Activity.id == activity_id).first()
        if not activity_info:
            return jsonify({"status": "failure", "message": "无效活动 ID"})
        openid = request.args.get("openid")
        activities_registration = ActivityParticipant.query. \
            filter(ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.participant_openid == openid).all()
        if not activities_registration:
            return jsonify({"status": "failure", "message": " 此人未报名"})
        return jsonify({"status": "success"})


class ActivityParticipantParser(object):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', type=str, location='headers', help='Open User ID')
        return parser

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', type=str, location='headers', help='Open User ID')
        parser.add_argument('activity_id', type=int, location='json', help='Activity ID')
        parser.add_argument('real_name', type=str, location='json', help='Real Name')
        parser.add_argument('id_type', type=str, location='json', help='ID Type')
        parser.add_argument('idcard', type=str, location='json', help='ID Card')
        parser.add_argument('email', type=str, location='json', help='email')
        parser.add_argument('paper_certificate', type=int, location='json', help='paper_certificate')
        parser.add_argument('recipient_name', type=str, location='json', help='Recipient Name')
        parser.add_argument('recipient_address', type=str, location='json', help='Recipient Address')
        parser.add_argument('recipient_phone', type=str, location='json', help='Recipient Phone')

        return parser


@activity.route("/activityParticipant", methods=["GET", 'POST'])
class ActivityParticipantRoot(Resource):
    @activity.expect(ActivityParticipantParser.get())
    def get(self):
        info = ActivityParticipantParser.get().parse_args()
        participant_openid = info.get('Authorization', None)

        activity_participant_infos = ActivityParticipant.query.all()
        logger.info("query all activity_participant info successfully")
        feedback = {"status": "success", "participant_openid": participant_openid, "activities": []}
        for activity_participant in activity_participant_infos:
            if activity_participant.participant_openid == participant_openid:
                logger.info(dbutils.serialize(activity_participant))
                activity_id = activity_participant.activity_id
                activity_info = Activity.query.filter(Activity.id == activity_id).first()
                activity_ = {"id": activity_info.id, "title": activity_info.title,
                             "location": activity_info.location}
                start = activity_info.start_time
                end = activity_info.end_time
                activity_["start_time"] = start.strftime("%Y-%m-%dT%H:%M:%S")
                activity_["end_time"] = end.strftime("%Y-%m-%dT%H:%M:%S")
                activity_["content"] = activity_info.content
                activity_["certificated"] = activity_participant.certificated
                activity_["current_state"] = activity_participant.current_state
                activity_["sign_method"] = activity_participant.sign_method
                if activity_participant.signup_time:
                    activity_["signup_time"] = activity_participant.signup_time.strftime("%Y-%m-%dT%H:%M:%S")
                    activity_["signup_latitude"] = str(activity_participant.signup_latitude)
                    activity_["signup_longtitude"] = str(activity_participant.signup_longitude)
                if activity_participant.signoff_time:
                    activity_["signoff_time"] = activity_participant.signoff_time.strftime("%Y-%m-%dT%H:%M:%S")
                    activity_["signoff_latitude"] = str(activity_participant.signoff_latitude)
                    activity_["signoff_longtitude"] = str(activity_participant.signoff_longitude)

                feedback["activities"].append(activity_)
        return jsonify(feedback)

    @activity.expect(ActivityParticipantParser.post())
    def post(self):
        info = ActivityParticipantParser.post().parse_args()
        logger.info("ActivityParticipantParser")
        logger.info(info)
        participant_openid = info.get('Authorization', None)
        activity_id = info.get("activity_id", None)
        real_name = info.get("real_name", None)
        id_type = info.get("id_type", None)
        idcard = info.get("idcard", None)
        email = info.get("email", None)
        paper_certificate = info.get("paper_certificate", None)
        activity_info = Activity.query.filter(Activity.id == activity_id).first()
        activity_title = activity_info.title
        start = activity_info.start_time
        end = activity_info.end_time
        activity_duration = (end - start).days * 24 + (end - start).seconds // 3600
        feedback = {"status": "success",
                    "participant_openid": participant_openid,
                    "activity_id": activity_id,
                    "activity_title": activity_title,
                    "real_name": real_name,
                    "id_type": id_type,
                    "idcard": idcard,
                    "email": email,
                    "paper_certificate": paper_certificate}
        logger.info(feedback)
        ActivityParticipant.query. \
            filter(ActivityParticipant.participant_openid == participant_openid,
                   ActivityParticipant.activity_id == activity_id). \
            update({ActivityParticipant.certificated: 0})
        activity_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.participant_openid == participant_openid).first()
        logger.info(activity_participant_info)

        certificated_user_info = User.query.filter(User.openid == participant_openid).first()
        certificated_user_info.real_name = real_name
        certificated_user_info.id_type = id_type
        certificated_user_info.idcard = idcard
        certificated_user_info.email = email

        certificated_info = {"paper_certificate": paper_certificate}
        if paper_certificate:
            recipient_name = info.get("recipient_name", None)
            recipient_address = info.get("recipient_address", None)
            recipient_phone = info.get("recipient_phone", None)
            certificated_user_info.recipient_name = recipient_name
            certificated_user_info.recipient_address = recipient_address
            certificated_user_info.recipient_phone = recipient_phone
            feedback["recipient_name"] = recipient_name
            feedback["recipient_address"] = recipient_address
            feedback["recipient_phone"] = recipient_phone
        if activity_participant_info and not activity_participant_info.certificated:
            certificated_info["certificated"] = 1
            certificated_info["certificate_date"] = datetime.now()
            activity_participant_info.paper_certificate = paper_certificate
            activity_participant_info.certificated = certificated_info["certificated"]
            activity_participant_info.certificate_date = certificated_info["certificate_date"]

            # update participant's related user info in user table
            logger.info(dbutils.serialize(activity_participant_info))
            logger.info(dbutils.serialize(certificated_user_info))
            db.session.commit()

            certification_info = {"name": real_name,
                                  "certificate_type": id_type,
                                  "certificate_code": idcard,
                                  "activity_title": activity_title,
                                  "activity_during": str(activity_duration) + "小时",
                                  "director": "王臻",
                                  "manager": "刘莉娟",
                                  "contact_code": "1388888888"}
            logger.info("certification_info")
            logger.info(certification_info)

            certification_file = certificationgenerate.generate_certification(certification_info)

            emailverify.send("email_resource/certificate-letter.html",
                             email, real_name + "'s certification",
                             "test", "12345678",
                             attachment_file=certification_file)

        return jsonify(feedback)


@activity.route("/myActivities", methods=["GET"])
class GetFavoriteActivities(Resource):
    def get(self):
        openid = request.headers.get("Authorization")
        target_filter = request.args.get("filter")
        if not target_filter or len(target_filter) == 0:
            target_filter = "all"

        favorite_activities_info = db.session.query(Activity.id, Activity.end_time). \
            filter(ActivityParticipant.participant_openid == openid). \
            filter(ActivityParticipant.interested == 1). \
            filter(ActivityParticipant.activity_id == Activity.id).all()
        registered_activities_info = db.session.query(Activity.id, Activity.end_time). \
            filter(ActivityParticipant.participant_openid == openid).\
            filter(ActivityParticipant.current_state.in_(('Registered', 'signed_up', 'signed_off'))). \
            filter(ActivityParticipant.activity_id == Activity.id).all()
        favorite_activities_info = [{'activity.id': i.id, 'activity.end_time': i.end_time}
                                    for i in favorite_activities_info] if favorite_activities_info else []
        registered_activities_info = [{'activity.id': j.id, 'activity.end_time': j.end_time}
                                      for j in registered_activities_info] if registered_activities_info else []

        target_activities_info = []
        if target_filter == "favorite":
            if favorite_activities_info is not None:
                for item in favorite_activities_info:
                    target_activities_info.append(item)
        elif target_filter == "registered":
            if registered_activities_info is not None:
                for item in registered_activities_info:
                    target_activities_info.append(item)
        elif target_filter == "all":
            id_set = []
            if favorite_activities_info is not None:
                for item in favorite_activities_info:
                    target_activities_info.append(item)
                    id_set.append(item["activity.id"])
            if registered_activities_info is not None:
                for item in registered_activities_info:
                    if item["activity.id"] not in id_set:
                        target_activities_info.append(item)
                        id_set.append(item["activity.id"])
        target_activities_info.sort(
            key=lambda item_: item_["activity.id"], reverse=True
        )
        target_activities_info = [
            item
            for item in target_activities_info
            if datetime.today() - timedelta(days=365) < item["activity.end_time"]
        ]

        queries = []
        for item in target_activities_info:
            activity_id = item["activity.id"]
            activity_ = Activity.query.filter(Activity.id == activity_id).first()
            activity_ = dbutils.serialize(activity_)
            queries.append(activitybiz.activity_converter(activity_, openid))
        return jsonify(queries)


class GetActivityParser(object):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', type=str, location='headers', help='Open User ID')
        parser.add_argument('activity_id', type=int, location='args', help='Activity ID')
        return parser


@activity.route("/activity_detail", methods=["GET"])
class GetActivity(Resource):
    @activity.expect(GetActivityParser().get())
    def get(self):
        """ get activity detail with activity_id """
        info = GetActivityParser.get().parse_args()
        openid = info.get("Authorization")
        activity_id = info.get("activity_id")

        logger.info("GetActivity: activity_id: %d, openid:%s", activity_id, openid)

        activity_info = Activity.query.filter(Activity.id == activity_id).first()
        if not activity_info:
            logger.warning("%d: no such activity", activity_id)
            return jsonify({"status": "failure", "message": "未知活动ID"})

        feedback = activitybiz.activity_converter(dbutils.serialize(activity_info), openid)
        feedback["status"] = "success"

        # Add activity participant details to user's query about his/her activity detail
        # Query participant details
        activity_participant = ActivityParticipant.query\
            .filter(ActivityParticipant.activity_id == activity_id,
                    ActivityParticipant.participant_openid == openid).first()
        if activity_participant:
            feedback["certificated"] = activity_participant.certificated
            feedback["current_state"] = activity_participant.current_state
            feedback["sign_method"] = activity_participant.sign_method
            if activity_participant.signup_time:
                feedback["signup_time"] = activity_participant.signup_time.strftime("%Y-%m-%dT%H:%M:%S")
                feedback["signup_latitude"] = str(activity_participant.signup_latitude)
                feedback["signup_longtitude"] = str(activity_participant.signup_longitude)
            if activity_participant.signoff_time:
                feedback["signoff_time"] = activity_participant.signoff_time.strftime("%Y-%m-%dT%H:%M:%S")
                feedback["signoff_latitude"] = str(activity_participant.signoff_latitude)
                feedback["signoff_longtitude"] = str(activity_participant.signoff_longitude)
            logger.info("%d: added activity participant dump successfully", activity_id)
        else:
            logger.info("%d: failed to added activity participant dump", activity_id)

        user_info = User.query.filter(User.openid == openid).first()
        if not user_info:
            feedback["status"] = "success"
            feedback["message"] = "未注册"
            return jsonify(feedback)
        if user_info.role == 0:  # 志愿者
            pickup_volunteer = db.session.query(PickupVolunteer). \
                filter(PickupVolunteer.openid == openid, PickupVolunteer.activity_id == activity_id).first()
            if pickup_volunteer:
                feedback['role'] = user_info.role
                feedback['needPickup'] = 1
                feedback['status'] = 'success'
                return jsonify(feedback)
        else:  # 视障人士
            pickup_impaired = db.session.query(PickupImpaired). \
                filter(PickupImpaired.openid == openid, PickupImpaired.activity_id == activity_id).first()
            if pickup_impaired:
                feedback['role'] = user_info.role
                feedback['needPickup'] = 1
                feedback['name'] = pickup_impaired.name
                feedback['idNo'] = pickup_impaired.id_no
                feedback['impairedNo'] = pickup_impaired.impaired_no
                feedback['pickupAddr'] = pickup_impaired.pickup_addr
                feedback['emergencyContact'] = pickup_impaired.emergency_contact
                feedback['status'] = 'success'
                return jsonify(feedback)
        feedback['needPickup'] = 0
        logger.info("%d: get activity successfully", activity_id)
        return jsonify(feedback)


@activity.route("/activity_detail/interest", methods=["POST"])
class MarkActivity(Resource):
    def post(self):
        """ mark activity as Interest """
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activity_id")
        interest = request.args.get("interest")
        feedback = {"status": "success"}
        activity_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.participant_openid == openid).first()
        if activity_participant_info:
            activity_participant_info.interested = interest
            # ActivityParticipant.query. \
            #     filter(ActivityParticipant.activity_id == activity_id,
            #            ActivityParticipant.participant_openid == openid). \
            #     update({ActivityParticipant.interested: interest})
            db.session.commit()
            return jsonify(feedback)
        else:
            activity_participant_info = ActivityParticipant()
            activity_participant_info.activity_id = activity_id
            activity_participant_info.participant_openid = openid
            activity_participant_info.interested = interest
            activity_participant_info.share = 0
            activity_participant_info.thumbs_up = 0
            db.session.add(activity_participant_info)
            db.session.commit()
            logger.info("Create new activity_participant_info successfully")
            return jsonify(feedback)


@activity.route("/activity_detail/thumbs_up", methods=["POST"])
class ThumbsUpActivity(Resource):
    def post(self):
        """mark activity as thumbs_up"""
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activity_id")
        thumbs_up = request.args.get("thumbs_up")
        feedback = {"status": "success"}
        activity_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.participant_openid == openid).first()
        if activity_participant_info:
            activity_participant_info.thumbs_up = thumbs_up
            db.session.commit()
            return jsonify(feedback)
        else:
            activity_participant_info = ActivityParticipant()
            activity_participant_info.activity_id = activity_id
            activity_participant_info.participant_openid = openid
            activity_participant_info.interested = 0
            activity_participant_info.share = 0
            activity_participant_info.thumbs_up = thumbs_up
            db.session.add(activity_participant_info)
            db.session.commit()
            logger.info("Create new activity_participant_info successfully")
            return jsonify(feedback)


@activity.route("/activity_detail/share", methods=["POST"])
class ShareActivity(Resource):
    def post(self):
        """ share activity """
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activity_id")
        participant = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.participant_openid == openid).all()
        if not participant:
            activity_participant_info = ActivityParticipant()
            activity_participant_info.activity_id = activity_id
            activity_participant_info.participant_openid = openid
            activity_participant_info.interested = 0
            activity_participant_info.share = 1
            activity_participant_info.thumbs_up = 0
            db.session.add(activity_participant_info)
            db.session.commit()
            logger.info("Create new activity_participant_info with share successfully")
            return jsonify({"status": "success"})

        participant = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.participant_openid == openid).first()
        if not participant:
            logger.warning("%d: no such activity", activity_id)
            return jsonify({"status": "failure"})

        share_count = int(participant.share)
        share_count += 1
        participant.share = share_count
        db.session.commit()
        return jsonify({"status": "success"})


class UserRegisterActivitiesParser(object):
    @staticmethod
    def common():
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', type=str, location='headers', help='Open User ID')
        parser.add_argument('activity_id', type=int, location='json', help='Activity ID')
        return parser


@activity.route("/activityParticipant/registerActivity", methods=["POST", 'DELETE'])
class UserRegisterActivities(Resource):
    @activity.expect(UserRegisterActivitiesParser().common())
    def post(self):
        # register an activity
        info = UserRegisterActivitiesParser.common().parse_args()
        openid = info.get('Authorization')
        activity_id = info.get('activity_id')

        logger.info('User %s register activity %s.' % (openid, activity_id))

        exist_registered_info = ActivityParticipant.query. \
            filter(ActivityParticipant.participant_openid == openid,
                   ActivityParticipant.activity_id == activity_id,
                   ActivityParticipant.current_state == 'Registered').first()
        if exist_registered_info:
            logger.info('Repeat registration.')
            return jsonify({"status": "failure", "message": "重复报名"})

        user_info = User.query.filter(User.openid == openid).first()
        if not user_info:
            return jsonify({"status": "failure", "message": "未能获取用户信息, 请先注册"})

        activity_info = db.session.query(Activity).filter(Activity.id == activity_id).first()
        if not activity_info:
            logger.error("Activity %d is not existing!", activity_id)
            return jsonify({"status": "failure", "message": "活动不存在"})

        exist_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.participant_openid == openid,
                   ActivityParticipant.activity_id == activity_id).first()
        if not exist_participant_info:
            activity_participant_info = ActivityParticipant()
            activity_participant_info.activity_id = activity_id
            activity_participant_info.participant_openid = openid
            activity_participant_info.interested = 0
            activity_participant_info.share = 0
            activity_participant_info.thumbs_up = 0
            activity_participant_info.current_state = "Registered"
            activity_participant_info.sign_method = "gps"
            activity_participant_info.certificated = 0
            activity_participant_info.certiticate_date = 0
            activity_participant_info.paper_certificate = 0
            db.session.add(activity_participant_info)
            db.session.commit()
            logger.info("OpenId:%s in activity:%s are inserted to activity_participant!", openid, activity_id)
        else:
            exist_participant_info.current_state = "Registered"
            exist_participant_info.sign_method = "gps"
            exist_participant_info.certificated = 0
            exist_participant_info.certiticate_date = 0
            exist_participant_info.paper_certificate = 0
            logger.info("OpenId:%s in activity:%s are updated to activity_participant!", openid, activity_id)
            db.session.commit()
        return jsonify({"status": "success"})

    @activity.expect(UserRegisterActivitiesParser().common())
    def delete(self):
        """ cancel specific registered activity """
        info = UserRegisterActivitiesParser.common().parse_args()
        openid = info.get('Authorization')
        activity_id = info.get('activity_id')

        logger.info('Delete openid - %s, activity id - %s' % (openid, activity_id))
        activity_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.participant_openid == openid,
                   ActivityParticipant.activity_id == activity_id).first()
        if activity_participant_info:
            activity_participant_info.current_state = None
            db.session.commit()
            logger.info("Deleted OpenId:%s with activity:%d in activity_participant!", openid, activity_id)

        activitybiz.user_cancel_activity(openid, activity_id)
        return jsonify({"status": "取消活动成功！"})


@activity.route("/pickUpImpaired", methods=["POST", "GET"])
class PickUpImpaired(Resource):
    def post(self):
        openid = request.headers.get('Authorization')
        data = request.get_json()
        activity_id = data['activity_id']
        pickup_info = db.session.query(PickupImpaired). \
            filter(PickupImpaired.openid == openid, PickupImpaired.activity_id == activity_id).first()
        if pickup_info:
            pickup_info.name = data['name']
            pickup_info.id_no = data['idNo']
            pickup_info.impaired_no = data['impairedNo']
            pickup_info.pickup_addr = data['pickupAddr']
            pickup_info.emergency_contact = data['emergencyContact']
            db.session.commit()
            return jsonify({'status': 'success', 'message': '更新成功'})
        new_pickup_info = PickupImpaired()
        new_pickup_info.openid = openid
        new_pickup_info.activity_id = activity_id
        new_pickup_info.name = data['name']
        new_pickup_info.id_no = data['idNo']
        new_pickup_info.impaired_no = data['impairedNo']
        new_pickup_info.pickup_addr = data['pickupAddr']
        new_pickup_info.emergency_contact = data['emergencyContact']
        db.session.add(new_pickup_info)
        db.session.commit()
        return jsonify({'status': 'success', 'message': '提交成功'})

    def get(self):
        # openid = request.headers.get('Authorization')
        # activity_id = request.args.get('activity_id')
        # logger.info('User %s get impaired pickup info map to %s.' % (openid, activity_id))
        # pickup_list = db.session.query(PickupImpaired). \
        #     filter(PickupImpaired.activity_id == activity_id).all()
        # return jsonify([dbutils.serialize(i) for i in pickup_list])
        volunteer_openid = request.headers.get('Authorization')
        activity_id = request.args.get('activity_id')
        need_pickup_impaired_participants = db.session. \
            query(PickupImpaired.name, PickupImpaired.pickup_addr, PickupImpaired.pickup_method,
                  User.avatar_url, User.openid). \
            filter(PickupImpaired.activity_id == activity_id,
                   PickupImpaired.openid == User.openid,
                   PickupImpaired.pickup_volunteer_openid.is_(None)).all()
        has_been_pickup_impaired_participants = db.session. \
            query(PickupImpaired.name, PickupImpaired.pickup_addr, PickupImpaired.pickup_method,
                  User.avatar_url, User.openid). \
            filter(PickupImpaired.activity_id == activity_id,
                   PickupImpaired.openid == User.openid,
                   PickupImpaired.pickup_volunteer_openid == volunteer_openid).all()
        need_pickup = [{'name': i[0], 'pickup_addr': i[1], 'pickup_method': i[2],
                        'avatar_url': i[3], 'openid': i[4]} for i in need_pickup_impaired_participants]
        already_pickup = [{'name': i[0], 'pickup_addr': i[1], 'pickup_method': i[2],
                           'avatar_url': i[3], 'openid': i[4]} for i in has_been_pickup_impaired_participants]
        need_pickup.extend(already_pickup)
        return jsonify(need_pickup)


@activity.route("/pickUpVolunteer", methods=["POST"])
class PickUpVolunteer(Resource):
    def post(self):
        openid = request.headers.get('Authorization')
        data = request.get_json()
        activity_id = data['activity_id']
        pickup_info = db.session.query(PickupVolunteer). \
            filter(PickupVolunteer.openid == openid, PickupVolunteer.activity_id == activity_id).first()
        if pickup_info:
            pickup_info.name = data['name']
            pickup_info.id_no = data['idNo']
            pickup_info.pickup_addr = data['pickupAddr']
            pickup_info.provide_service = data['provideService']
            db.session.commit()
            return jsonify({'status': 'success', 'message': '更新成功'})
        new_pickup_info = PickupVolunteer()
        new_pickup_info.openid = openid
        new_pickup_info.activity_id = activity_id
        new_pickup_info.name = data['name']
        new_pickup_info.id_no = data['idNo']
        new_pickup_info.pickup_addr = data['pickupAddr']
        new_pickup_info.provide_service = data['provideService']
        db.session.add(new_pickup_info)
        db.session.commit()
        return jsonify({'status': 'success', 'message': '提交成功'})


class SignupParser(object):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', type=str, location='headers', help='Open User ID')
        parser.add_argument('activity_id', type=int, location='json', help='Activity ID')
        parser.add_argument('sign_method', type=str, location='json', help='sign methods:token/gps')
        parser.add_argument('signup_time', type=str, location='json', help='sign up time')
        parser.add_argument('signup_latitude', type=float, location='json', help='sign up latitude')
        parser.add_argument('signup_longitude', type=float, location='json', help='sign up longitude')
        return parser


@activity.route("/activityParticipant/signup", methods=["POST"])
class SignupActivity(Resource):
    @activity.expect(SignupParser.post())
    def post(self):
        """Sign up an activity"""
        new_info = SignupParser.post().parse_args()
        # new_info = {'Authorization': 'om68340DDXrYTpfKM6SuM6XTm44s',
        #         'activity_id':10,
        #         'signup_time':'2021-02-10 14:25:09',
        #         'signup_latitude':31.2,
        #         'signup_longitude':121.3
        #         }
        openid = new_info.get("Authorization")
        activity_id = new_info.get("activity_id")
        if not activity_id:
            logger.info('Loading participant %s sign up activity %d info ...', openid, activity_id)
        else:
            logger.error('Loading participant %s sign up activity None detected ...', openid)

        activity_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.participant_openid == openid, ActivityParticipant.activity_id == activity_id).first()
        if activity_participant_info:
            activity_participant_info.signup_time = new_info.get("signup_time")
            activity_participant_info.signup_latitude = new_info.get("signup_latitude")
            activity_participant_info.signup_longitude = new_info.get("signup_longitude")
            activity_participant_info.sign_method = new_info.get("sign_method")
            activity_participant_info.current_state = "signed_up"
            db.session.commit()
            logger.info("%s in %d: update activity_participant successfully", openid, activity_id)
            return jsonify({"status": "success"})

        activity_info = db.session.query(Activity). \
            filter(Activity.id == activity_id).first()
        if not activity_info:
            logger.error('Failed to query activity %d info ...', activity_id)
            return jsonify({"status": "failure"})

        activity_participant_info = ActivityParticipant()
        activity_participant_info.activity_id = activity_id
        activity_participant_info.participant_openid = openid
        activity_participant_info.interested = 0
        activity_participant_info.share = 0
        activity_participant_info.thumbs_up = 0
        activity_participant_info.certificated = 0
        activity_participant_info.certiticate_date = 0
        activity_participant_info.paper_certificate = 0
        activity_participant_info.signup_time = new_info.get("signup_time")
        activity_participant_info.signup_latitude = new_info.get("signup_latitude")
        activity_participant_info.signup_longitude = new_info.get("signup_longitude")
        activity_participant_info.sign_method = new_info.get("sign_method")
        activity_participant_info.current_state = "signed_up"
        db.session.add(activity_participant_info)
        db.session.commit()

        return jsonify({"status": "success"})


class SignoffParser(object):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', type=str, location='headers', help='Open User ID')
        parser.add_argument('activity_id', type=int, location='json', help='Activity ID')
        parser.add_argument('sign_method', type=str, location='json', help='sign methods:token/gps')
        parser.add_argument('signoff_time', type=str, location='json', help='sign off time')
        parser.add_argument('signoff_latitude', type=float, location='json', help='sign off latitude')
        parser.add_argument('signoff_longitude', type=float, location='json', help='sign off longitude')
        return parser


@activity.route("/activityParticipant/signoff", methods=['POST'])
class SignoffActivity(Resource):
    @activity.expect(SignoffParser.post())
    def post(self):
        """Sign off an activity"""
        new_info = SignoffParser.post().parse_args()
        # new_info = {'Authorization': 'om68340DDXrYTpfKM6SuM6XTm44s',
        #         'activity_id':10,
        #         'signoff_time':'2021-02-10 14:25:09',
        #         'signoff_latitude':31.2,
        #         'signoff_longitude':121.3
        #         }
        openid = new_info.get('Authorization')
        activity_id = new_info.get('activity_id')
        logger.info('Loading participant sign up info ...')

        activity_participant_info = db.session.query(ActivityParticipant). \
            filter(ActivityParticipant.participant_openid == openid, ActivityParticipant.activity_id == activity_id).first()
        if activity_participant_info:
            activity_participant_info.signoff_time = new_info.get("signoff_time")
            activity_participant_info.signoff_latitude = new_info.get("signoff_latitude")
            activity_participant_info.signoff_longitude = new_info.get("signoff_longitude")
            activity_participant_info.sign_method = new_info.get("sign_method")
            activity_participant_info.current_state = "signed_off"
            db.session.commit()
            logger.info("%s in %d: update activity successfully", openid, activity_id)
            return jsonify({"status": "success"})

        logger.info("user_openid %s in activity %d not found", openid, activity_id)
        return jsonify({"status": "failure"})


@activity.route("/activityParticipant/pickupDetailInfo", methods=['POST', 'GET'])
class PickupDetailInfo(Resource):
    def get(self):
        volunteer_openid = request.headers.get('Authorization')
        activity_id = request.args.get('activity_id')
        need_pickup_impaired_participants = db.session. \
            query(PickupImpaired.name, PickupImpaired.pickup_addr, PickupImpaired.pickup_method,
                  User.avatar_url, User.openid). \
            filter(PickupImpaired.activity_id == activity_id,
                   PickupImpaired.openid == User.openid,
                   PickupImpaired.pickup_volunteer_openid.is_(None)).all()
        has_been_pickup_impaired_participants = db.session. \
            query(PickupImpaired.name, PickupImpaired.pickup_addr, PickupImpaired.pickup_method,
                  User.avatar_url, User.openid). \
            filter(PickupImpaired.activity_id == activity_id,
                   PickupImpaired.openid == User.openid,
                   PickupImpaired.pickup_volunteer_openid == volunteer_openid).all()
        need_pickup = [{'name': i[0], 'pickup_addr': i[1], 'pickup_method': i[2],
                        'avatar_url': i[3], 'openid': i[4]} for i in need_pickup_impaired_participants]
        already_pickup = [{'name': i[0], 'pickup_addr': i[1], 'pickup_method': i[2],
                           'avatar_url': i[3], 'openid': i[4]} for i in has_been_pickup_impaired_participants]
        need_pickup.extend(already_pickup)
        return jsonify(need_pickup)

    def post(self):
        new_volunteer_openid = request.headers.get('Authorization')
        data = request.get_json()
        activity_id = data['activity_id']
        impaired_openid = data['impairedOpenid']
        new_pickup_method = data['pickupMethod']
        pickup_info = db.session.query(PickupImpaired).\
            filter(PickupImpaired.openid == impaired_openid,
                   PickupImpaired.activity_id == activity_id).first()
        old_pickup_method = pickup_info.pickup_method
        old_pickup_volunteer = pickup_info.pickup_volunteer_openid
        if old_pickup_method == new_pickup_method == "":
            return {'status': 'success', 'message': '用户未操作'}
        if old_pickup_method != new_pickup_method or old_pickup_volunteer != new_volunteer_openid:
            # pickup info changed
            pickup_info.pickup_method = new_pickup_method
            pickup_info.pickup_volunteer_openid = new_volunteer_openid
            activitybiz.volunteer_pickup_impaired(new_volunteer_openid, impaired_openid, new_pickup_method)
            if not new_pickup_method:
                pickup_info.pickup_volunteer_openid = None
            db.session.commit()
        return {'status': 'success', 'message': 'Pickup Success'}

class ExportSignParser(object):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('activity_id', type=int)

        return parser

@activity.route("/activity/export/sign", methods=['GET'])
class ExportSign(Resource):
    @activity.expect(ExportSignParser.get())
    def get(self):
        info = ExportSignParser.get().parse_args()
        activity_id = info.get('activity_id')

        activity = db.session.query(Activity).filter_by(id=activity_id).first()

        xls = activitybiz.form_sign(activity)

        filename = f'{activity.title}({activity.start_date})签到签收表.xlsx'
        return send_file(xls,
                as_attachment=True,
                attachment_filename=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

class ExportSummaryParser(object):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d'), required=True)
        parser.add_argument('end_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d'), required=True)

        return parser

@activity.route("/activity/export/duty_summary", methods=['GET'])
class ExportDutySummary(Resource):
    @activity.expect(ExportSummaryParser.get())
    def get(self):
        return gen_summary_form(activitybiz.form_duty_summary,
                '活动职责汇总')

@activity.route("/activity/export/info_summary", methods=['GET'])
class ExportInfoSummary(Resource):
    @activity.expect(ExportSummaryParser.get())
    def get(self):
        return gen_summary_form(activitybiz.form_info_summary,
                '活动汇总信息')

def gen_summary_form(generate_func, subject):
    info = ExportSummaryParser.get().parse_args()
    start_date = info.get('start_date')
    end_date = info.get('end_date')
    activities = db.session.query(Activity).filter(Activity.start_time >= start_date, Activity.start_time <= end_date + timedelta(days=1)).all()

    # for a in activities:
    #     print([i.gifts for i in a.participate_infos], file=sys.stderr)
    xls = generate_func(activities)

    filename = f'{start_date.strftime("%Y-%m-%d")} ~ {end_date.strftime("%Y-%m-%d")}{subject}.xlsx'

    return send_file(xls,
            as_attachment=True,
            attachment_filename=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@activity.route("/activity/projects", methods=['GET'])
class GetProjects(Resource):
    def get(self):
        projects = db.session.query(Project).all()
        return jsonify({
            'status': 'success',
            'data': [x.to_json() for x in projects]
        })

@activity.route("/activity/duties", methods=['GET'])
class GetDuties(Resource):
    def get(self):
        duties = db.session.query(Duty).all()
        return jsonify({
            'status': 'success',
            'data': [x.to_json() for x in duties]
        })

@activity.route("/activity/gifts", methods=['GET'])
class GetGifts(Resource):
    def get(self):
        gifts = db.session.query(Gift).all()
        return jsonify({
            'status': 'success',
            'data': [x.to_json() for x in gifts]
        })

@activity.route("/activity/review/<int:activity_id>", methods=['POST'])
class ReviewActivity(Resource):
    def post(self, activity_id):
        activity = Activity.query.filter(Activity.id == activity_id).first()
        if activity is None:
            return {
                "status": "failure",
                "error": "活动不存在"
            }, 404

        data = request.get_json()['data']
        if not data or len(data) == 0:
            return {
                "status": "failure",
                "error": "活动参与情况不能为空"
            }, 400

        info_map = dict([(info.phone, info) for info in activity.participate_infos])
        for item in data:
            # TODO insert new
            if info_map.get(item['phone']) is None:
                continue
            # TODO check if info.user matches

            info = info_map[item['phone']]
            info.remark = item['remark']
            # TODO check if id exists
            info.duties = item['duties']
            info.gifts = item['gifts']
            db.session.add(info)

        db.session.commit()
        return jsonify({
            'status': 'success',
        })
