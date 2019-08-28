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


/* admin table */
create table admin
(
    id                  INT                 NOT NULL AUTO_INCREMENT,
    registration_date   DATE                NOT NULL,
    user_name           VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    passwd              BINARY(60)          NOT NULL,
    real_name           VARCHAR(8)          NOT NULL,
    gender              CHAR(1)             NOT NULL,
    phone               VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    phone_verified      BIT(1)              NOT NULL        DEFAULT 0,
    email               VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    email_verified      BIT(1)              NOT NULL        DEFAULT 0,

    PRIMARY KEY (id)
);


/* volunteer table */
create table volunteer
(
    openid                      CHAR(28)            NOT NULL,
    registration_date           DATE                NOT NULL,
    user_name                   VARCHAR(60)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    password                    BINARY(60)          NOT NULL,
    real_name                   VARCHAR(8)          NOT NULL,
    id_card                     CHAR(18)            NOT NULL UNIQUE,
    id_card_verified            BIT(1)              NOT NULL        DEFAULT 0,
    phone                       VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    phone_verified              BIT(1)              NOT NULL        DEFAULT 0,
    email                       VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    email_verified              BIT(1)              NOT NULL        DEFAULT 0,
    gender                      CHAR(1)             NOT NULL,
    birth                       DATE                NOT NULL,
    address                     VARCHAR(100)        NOT NULL,
    emergent_contact            VARCHAR(8),
    emergent_contact_phone      VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    emergent_contact_verified   BIT(1)              NOT NULL        DEFAULT 0,
    ppl_served                  INT                 NOT NULL        DEFAULT 0,
    activities_joined           SMALLINT            NOT NULL        DEFAULT 0,
    experience                  BIGINT              NOT NULL        DEFAULT 0,
    level                       SMALLINT            NOT NULL        DEFAULT 0,
    wxappid                     CHAR(16)            NOT NULL        DEFAULT '92cd67eef330384f',
    wxsccret                    CHAR(32)            NOT NULL        DEFAULT 'f8c54009768cfd81e3533583651b7dfd',

    PRIMARY KEY (openid)
);


/* vision-impaired table */
create table vision_impaired
(
    openid                      CHAR(28)            NOT NULL,
    registration_date           DATE                NOT NULL,
    user_name                   VARCHAR(60)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    password                    BINARY(60)          NOT NULL,
    real_name                   VARCHAR(8)          NOT NULL,
    id_card                     CHAR(18)            NOT NULL UNIQUE,
    id_card_verified            BIT(1)              NOT NULL        DEFAULT 0,
    disabled_id                 VARCHAR(60)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    disabled_id_verified        BIT(1)              NOT NULL        DEFAULT 0,
    phone                       VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    phone_verified              BIT(1)              NOT NULL        DEFAULT 0,
    email                       VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    email_verified              BIT(1)              NOT NULL        DEFAULT 0,
    gender                      CHAR(1)             NOT NULL,
    birth                       DATE                NOT NULL,
    address                     VARCHAR(100)        NOT NULL,
    emergent_contact            VARCHAR(8)          NOT NULL,
    emergent_contact_phone      VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    emergent_contact_verified   BIT(1)              NOT NULL        DEFAULT 0,
    activities_joined           INT                 NOT NULL        DEFAULT 0,
    paired_volunteers           SMALLINT            NOT NULL        DEFAULT 0,
    experience                  BIGINT              NOT NULL        DEFAULT 0,
    level                       SMALLINT            NOT NULL        DEFAULT 0,
    wxappid                     CHAR(16)            NOT NULL        DEFAULT '92cd67eef330384f',
    wxsccret                    CHAR(32)            NOT NULL        DEFAULT 'f8c54009768cfd81e3533583651b7dfd',

    PRIMARY KEY(openid)
);


/* activity table */
create table activity
(
    id                          BIGINT              NOT NULL AUTO_INCREMENT,
    name                        VARCHAR(200)        NOT NULL        DEFAULT '助盲公益活动',
    time                        DATETIME            NOT NULL,
    address                     VARCHAR(100)        NOT NULL,
    duration                    TIME                NOT NULL        DEFAULT '3:00:00',
    description                 TEXT                NOT NULL,
    matter_attention            TEXT                NOT NULL,
    remark                      VARCHAR(120)        NOT NULL        DEFAULT '助盲公益活动备注',
    approved                    BIT(1)              NOT NULL        DEFAULT 0,
    approver_id                 INT,
    assiged                     BIT(1)              NOT NULL        DEFAULT 0,
    assignee_openid             CHAR(28),
    published                   BIT(1)              NOT NULL        DEFAULT 0,

    FOREIGN KEY (approver_id) REFERENCES admin(id),
    FOREIGN KEY (assignee_openid) REFERENCES volunteer(openid),

    PRIMARY KEY (id)
);


/* activity case table */
create table activity_case
(
    case_id                     BIGINT              NOT NULL AUTO_INCREMENT,
    raiser_openid               CHAR(28),
    raiser_adminid              INT,
    raiser_type                 VARCHAR(16)         NOT NULL        DEFAULT 'admin',
    need_pickup                 BIT(1)              NOT NULL        DEFAULT 0,
    offer_pickup                BIT(1)              NOT NULL        DEFAULT 0,
    pickups                     TINYINT             NOT NULL        DEFAULT 1,
    sign_in_status              BIT(1)              NOT NULL        DEFAULT 0,

    FOREIGN KEY (raiser_openid) REFERENCES volunteer(openid),
    FOREIGN KEY (raiser_adminid) REFERENCES admin(id),

    PRIMARY KEY (case_id)
);
