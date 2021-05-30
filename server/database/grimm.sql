/*
 * File: grimm.sql
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
DROP    DATABASE IF EXISTS      grimmdb;
CREATE  DATABASE IF NOT EXISTS  grimmdb;
/* Selecting database */
USE grimmdb;


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
    id                  INT                 NOT NULL,  /* 0 是 root 用户 */
    registration_date   DATE                NOT NULL,
    password            BINARY(60)          NOT NULL    DEFAULT 0,
    name                VARCHAR(100),
    email               VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE,
    email_verified      TINYINT             DEFAULT 0,

    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO admin (id, registration_date, password, name, email_verified, email)
VALUES (0, NOW(), 'default', 'root', 1, 'no.reply@rp-i.org');

/* user table */
create table user
(
    openid                      CHAR(28)            NOT NULL,
    registration_date           DATE                NOT NULL,
    role                        TINYINT             NOT NULL        DEFAULT 0,  /* 0 是志愿者， 1 是视障人士 */
    name                        VARCHAR(100)        DEFAULT "志愿者",
    real_name                   VARCHAR(100),
    id_type                     VARCHAR(100)        DEFAULT "身份证",
    idcard                      CHAR(18)            UNIQUE,
    idcard_verified             TINYINT             DEFAULT 0,
    disabled_id                 VARCHAR(60)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE ,
    disabled_id_verified        TINYINT             DEFAULT 0,
    phone                       VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    phone_verified              TINYINT             NOT NULL        DEFAULT 0,
    email                       VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE,
    email_verified              TINYINT             DEFAULT 0,
    contact                     VARCHAR(16)         DEFAULT NULL,
    gender                      CHAR(1)             NOT NULL        DEFAULT "无",
    birth                       DATE                NOT NULL,
    address                     VARCHAR(80)         DEFAULT "无",
    emergent_contact            VARCHAR(8)          DEFAULT NULL,
    emergent_contact_phone      VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
    activities_joined           SMALLINT            NOT NULL        DEFAULT 0,
    activities_absence          SMALLINT            NOT NULL        DEFAULT 0,
    remark                      VARCHAR(255)        DEFAULT "无",
    audit_status                TINYINT             NOT NULL        DEFAULT 0,
    push_status                 TINYINT             NOT NULL        DEFAULT 0,
    recipient_name              VARCHAR(100),
    recipient_address           VARCHAR(80),
    recipient_phone             VARCHAR(16),

    PRIMARY KEY (openid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


/* activity table */
create table activity
(
    id                          BIGINT              NOT NULL        AUTO_INCREMENT,
    title                       VARCHAR(60)         NOT NULL        DEFAULT '助盲公益活动',
    start_time                  DATETIME            NOT NULL,
    location                    VARCHAR(100)        NOT NULL,
    end_time                    DATETIME,
    content                     TEXT                NOT NULL,
    notice                      TEXT,
    others                      VARCHAR(120)        NOT NULL        DEFAULT '无',
    admin_raiser                INT                 DEFAULT NULL,
    user_raiser                 CHAR(28),
    approver                    INT                 DEFAULT NULL,
    assignee                    CHAR(28),
    published                   TINYINT             NOT NULL        DEFAULT 0,
    tag_ids                     VARCHAR(120),
    volunteer_capacity          INT                 DEFAULT 0,
    vision_impaired_capacity    INT                 DEFAULT 0,
    volunteer_job_title         TEXT,
    volunteer_job_content       TEXT,
    activity_fee                INT                 DEFAULT 0,
    sign_in_radius              INT                 DEFAULT NULL,

    FOREIGN KEY (user_raiser) REFERENCES user(openid)
    ON DELETE set null
    ON UPDATE cascade,
    FOREIGN KEY (admin_raiser) REFERENCES admin(id)
    ON DELETE set null
    ON UPDATE cascade,
    FOREIGN KEY (approver) REFERENCES admin(id)
    ON DELETE set null
    ON UPDATE cascade,
    FOREIGN KEY (assignee) REFERENCES user(openid)
    ON DELETE set null
    ON UPDATE cascade,

    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


/* registered activities table */
create table registered_activity
(
    user_openid                 CHAR(28)            NOT NULL,
    activity_id                 BIGINT              NOT NULL,
    phone                       VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    address                     VARCHAR(80)         NOT NULL,
    needpickup                  TINYINT             NOT NULL        DEFAULT 0,
    topickup                    TINYINT             NOT NULL        DEFAULT 0,
    accepted                    TINYINT             NOT NULL        DEFAULT -1,

    FOREIGN KEY (user_openid) REFERENCES user(openid)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activity(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    INDEX(user_openid, activity_id),

    PRIMARY KEY(user_openid, activity_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* pickup table */
create table pickup_pair
(
    activity_id                 BIGINT,
    offer                       CHAR(28)            NOT NULL,
    need                        CHAR(28)            NOT NULL,
    time                        DATETIME            NOT NULL,
    location                    VARCHAR(100)        NOT NULL,

    FOREIGN KEY (activity_id) REFERENCES activity(id)
    ON DELETE cascade
    ON UPDATE cascade,
    FOREIGN KEY (offer) REFERENCES user(openid)
    ON DELETE cascade
    ON UPDATE cascade,
    FOREIGN KEY (need) REFERENCES user(openid)
    ON DELETE cascade
    ON UPDATE cascade,

    PRIMARY KEY(offer, need)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


create table activity_participant
(
    activity_id                 BIGINT,
    participant_openid          CHAR(28)            NOT NULL, 
    interested                  TINYINT             DEFAULT 0,
    share                       INT                 DEFAULT 0,
    thumbs_up                   TINYINT             DEFAULT 0,
    certificated                TINYINT,
    certificate_date            DATE,
    paper_certificate           TINYINT,
    
    FOREIGN KEY (activity_id) REFERENCES activity(id)
    ON DELETE cascade
    ON UPDATE cascade,
    FOREIGN KEY (participant_openid) REFERENCES user(openid)
    ON DELETE cascade
    ON UPDATE cascade,

    PRIMARY KEY(activity_id, participant_openid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

