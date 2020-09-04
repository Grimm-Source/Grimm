#
# File: db_utils.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Albert Yang(alberyan@cisco.com)
#
# Description: Simple db operation
#
# To-Dos:
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#
#

import server.core.db as db
import server.utils.tag_converter as tag_converter
from server.utils.misctools import calc_duration


def get_total_share(activity_id):
    share = db.expr_query(
        "activity_participants",
        "COUNT(*)",
        clauses="activity_participants.activity_id = {} "
        "and activity_participants.share = 1".format(activity_id),
    )[0]["COUNT(*)"]
    if share is None:
        return 0
    return share


def get_total_interested(activity_id):
    interested = db.expr_query(
        "activity_participants",
        "COUNT(*)",
        clauses="activity_participants.activity_id = {} "
        "and activity_participants.interested = 1".format(activity_id),
    )[0]["COUNT(*)"]
    if interested is None:
        return 0
    return interested


def get_total_thumbs_up(activity_id):
    thumbs_up = db.expr_query(
        "activity_participants",
        "COUNT(*)",
        clauses="activity_participants.activity_id = {} "
        "and activity_participants.thumbs_up = 1".format(activity_id),
    )[0]["COUNT(*)"]
    if thumbs_up is None:
        return 0
    return thumbs_up


def get_total_registered(activity_id):
    registered = db.expr_query(
        "registerActivities",
        "COUNT(*)",
        clauses="registerActivities.activity_id = {}".format(activity_id),
    )[0]["COUNT(*)"]
    if registered is None:
        return 0
    return registered

def convert_db_activity_to_http_query(activity):
    query = {}
    activity_id = activity["activity_id"]
    query["id"] = activity_id
    query["adminId"] = activity["approver"]
    query["title"] = activity["title"]
    query["location"] = activity["location"]
    start = activity["start_time"]
    end = activity["end_time"]
    query["start_time"] = start.strftime("%Y-%m-%dT%H:%M:%S")
    query["end_time"] = end.strftime("%Y-%m-%dT%H:%M:%S")
    query["duration"] = calc_duration(start, end)
    query["content"] = activity["content"]
    query["notice"] = activity["notice"]
    query["others"] = activity["others"]
    query["tag"] = tag_converter.convert_idstring_to_tagstring(activity["tag_ids"])
    query["share"] = get_total_share(activity_id)
    query["interested"] = get_total_interested(activity_id)
    query["thumbs_up"] = get_total_thumbs_up(activity_id)
    query["registered"] = get_total_registered(activity_id)
    query["volunteer_capacity"] = activity["volunteer_capacity"]
    query["is_volunteer_limited"] = True if (activity["volunteer_capacity"] is not None and activity["volunteer_capacity"] > 0) else False
    query["vision_impaired_capacity"] = activity["vision_impaired_capacity"]
    query["is_impaired_limited"] = True if (activity["vision_impaired_capacity"] is not None and activity["vision_impaired_capacity"] > 0) else False
    query["volunteer_job_title"] = activity["volunteer_job_title"]
    query["volunteer_job_content"] = activity["volunteer_job_content"]
    query["activity_fee"] = activity["activity_fee"]
    query["is_fee_needed"] = True if (activity["activity_fee"] is not None and activity["activity_fee"] > 0) else False

    return query