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
    admin_id            INT                 NOT NULL,  /* 0 是 root 用户 */
    registration_date   DATE                NOT NULL,
    password            BINARY(60)          NOT NULL    DEFAULT 0,
    name                VARCHAR(8),
    email               VARCHAR(32)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE,
    email_verified      TINYINT             DEFAULT 0,

    PRIMARY KEY (admin_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO admin (admin_id, registration_date, password, name, email_verified, email)
VALUES (0, NOW(), 'default', 'root', 1, 'no.reply@rp-i.org');

/* user table */
create table user
(
    openid                      VARCHAR(35)         NOT NULL,
    registration_date           DATE                NOT NULL,
    role                        TINYINT             NOT NULL        DEFAULT 0,  /* 0 是志愿者， 1 是视障人士 */
    name                        VARCHAR(8)          DEFAULT "志愿者",
    idcard                      CHAR(18)            UNIQUE,
    idcard_verified             TINYINT             DEFAULT 0,
    disabled_id                 VARCHAR(60)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin UNIQUE,
    disabled_id_verified        TINYINT             DEFAULT 0,
    phone                       VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    phone_verified              TINYINT             NOT NULL        DEFAULT 0,
    contact                     VARCHAR(16),
    gender                      CHAR(1)             NOT NULL,
    birth                       DATE                NOT NULL,
    address                     VARCHAR(80)         NOT NULL,
    emergent_contact            VARCHAR(8),
    emergent_contact_phone      VARCHAR(16)         CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
    activities_joined           SMALLINT            NOT NULL        DEFAULT 0,
    remark                      VARCHAR(100)        DEFAULT "无",
    audit_status                TINYINT             NOT NULL        DEFAULT 0,

    PRIMARY KEY (openid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO user (openid, registration_date, idcard, phone, phone_verified, gender, birth, address, emergent_contact, emergent_contact_phone, role, contact)
VALUES ('0', NOW(), '000000000000000000', '13163236603', 1, '女', '1979-09-19', "湖北省武汉市洪山区", "张三", "17621533767", 0, '021-08131311');

INSERT INTO user (openid, registration_date, idcard, phone, phone_verified, gender, birth, address, emergent_contact, emergent_contact_phone, name, role, contact)
VALUES ('1', NOW(), '111111111111111111', '13163236604', 1, '男', '1985-08-14', "湖北省武汉市武昌区", "李四", "18256789090", "视障人士", 1, '021-08131311');


/* activity table */
create table activity
(
    activity_id                 BIGINT              NOT NULL AUTO_INCREMENT,
    title                       VARCHAR(200)        NOT NULL        DEFAULT '助盲公益活动',
    start_time                  DATETIME            NOT NULL,
    location                    VARCHAR(100)        NOT NULL,
    end_time                    DATETIME,
    content                     TEXT                NOT NULL,
    notice                      TEXT,
    others                      VARCHAR(120)        NOT NULL        DEFAULT '无',
    admin_raiser                INT                 DEFAULT NULL,
    user_raiser                 VARCHAR(35),
    approver                    INT                 DEFAULT NULL,
    assignee                    VARCHAR(35),
    published                   TINYINT             NOT NULL        DEFAULT 0,

    FOREIGN KEY (user_raiser) REFERENCES user(openid)
    ON DELETE set null
    ON UPDATE cascade,
    FOREIGN KEY (admin_raiser) REFERENCES admin(admin_id)
    ON DELETE set null
    ON UPDATE cascade,
    FOREIGN KEY (approver) REFERENCES admin(admin_id)
    ON DELETE set null
    ON UPDATE cascade,
    FOREIGN KEY (assignee) REFERENCES user(openid)
    ON DELETE set null
    ON UPDATE cascade,

    PRIMARY KEY (activity_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO activity (start_time, location, content, notice, user_raiser, approver, assignee, end_time)
VALUES (NOW(), "湖北省宜昌市夷陵区", "爱心牵手，你我同行", "需要配备雨具", '0', 0, '1', '2019-10-28 09:30:00');


/* pickup table */
create table pickups
(
    activity_id                 BIGINT,
    offer_pickup                VARCHAR(35)         NOT NULL,
    need_pickup                 VARCHAR(35)         NOT NULL,
    time                        DATETIME            NOT NULL,
    location                    VARCHAR(100)        NOT NULL,

    FOREIGN KEY (activity_id) REFERENCES activity(activity_id)
    ON DELETE cascade
    ON UPDATE cascade,
    FOREIGN KEY (offer_pickup) REFERENCES user(openid)
    ON DELETE cascade
    ON UPDATE cascade,
    FOREIGN KEY (need_pickup) REFERENCES user(openid)
    ON DELETE cascade
    ON UPDATE cascade,

    PRIMARY KEY(offer_pickup, need_pickup)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO pickups (activity_id, offer_pickup, need_pickup, time, location)
VALUES (1, '0', '1', NOW(), "上海市某个地方");
