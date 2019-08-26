/*
 * File: Grimm.sql
 * Copyright: grimm Project, Ren Pin NGO, all rights reserved.
 * License: MIT
 * -------------------------------------------------------------------------
 * Authors:  Ming Li(adagio.ming@gmail.com)
 *
 * Description: Mysql script for server db back-end.
 *
 * To-Dos:
 *   1. make other supplements if needed.
 *
 * Issues:
 *   No issue so far.
 *
 * Revision History (Date, Editor, Description):
 *   1. 2019/08/15, Ming, create first revision.
 *
 */



/* Creating database */
DROP    DATABASE IF EXISTS      grimm;
CREATE  DATABASE IF NOT EXISTS  grimm;
/* Selecting database */
USE grimm;


/* Configuring character_set */
SET character_set_client        = utf8mb4;
SET character_set_connection    = utf8mb4;
SET character_set_database      = utf8mb4;
SET character_set_filesystem    = binary;
SET character_set_results       = utf8mb4;
SET character_set_server        = utf8mb4;


/* Creating tables */
create table admin
(
    usr_id          BIGINT  UNSIGNED    PRIMARY KEY, /* this is for user index in DB only */
    account         VARCHAR(32)         NOT NULL UNIQUE,
    passwd          BINARY(60)          NOT NULL,    /* we don't preserve user password, we only preserve HASH value */
    register_date   DATE                NOT NULL
);


create table volunteer
(
);

create table vision-impaired
(
);


create table event
(
);
