#
# File: tag_converter.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Albert Yang(alberyan@cisco.com)
#
# Description: do tag conversion between string and array.
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
from server import admin_logger

def convert_ids_to_tags(ids):
    tag_list = []
    tags_map = get_tags_map()
    for id in ids.split(","):
        tag_list.append(tags_map[id])
    return tag_list

def convert_tags_to_ids(tags_list):
    id_list = []
    reverse_tags_map = get_reverse_tags_map()
    for tag in tags_list:
        id_list.append(reverse_tags_map[tag])
    return ','.join(id_list)

def get_tags_map():
    try:
        tags_table = db.expr_query('activity_tag')
    except:
        admin_logger.warning('get activity tag failed')
    tags_map = {}
    for pair in tags_table:
        tags_map[pair['tag_id']] = pair['tag_name']
    return tags_map

def get_reverse_tags_map():
    try:
        tags_table = db.expr_query('activity_tag')
    except:
        admin_logger.warning('get activity tag failed')
    reverse_tags_map = {}
    for pair in tags_table:
        reverse_tags_map[pair['tag_name']] = pair['tag_id']
    return reverse_tags_map