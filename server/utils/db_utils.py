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
