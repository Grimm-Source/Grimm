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
    return db.expr_query(
        "activity_participants",
        "COUNT(*)",
        clauses="activity_participants.activity_id = {} "
        "and activity_participants.share = 1".format(activity_id),
    )[0]["COUNT(*)"]


def get_total_interested(activity_id):
    return db.expr_query(
        "activity_participants",
        "COUNT(*)",
        clauses="activity_participants.activity_id = {} "
        "and activity_participants.interested = 1".format(activity_id),
    )[0]["COUNT(*)"]


def get_total_thumbs_up(activity_id):
    return db.expr_query(
        "activity_participants",
        "COUNT(*)",
        clauses="activity_participants.activity_id = {} "
        "and activity_participants.thumbs_up = 1".format(activity_id),
    )[0]["COUNT(*)"]


def get_total_registered(activity_id):
    return db.expr_query(
        "registerActivities",
        "COUNT(*)",
        clauses="registerActivities.activity_id = {}".format(activity_id),
    )[0]["COUNT(*)"]
