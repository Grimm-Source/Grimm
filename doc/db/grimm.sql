/*
Navicat MySQL Data Transfer

Copyright             : grimm Project, Ren Pin NGO, all rights reserved.
License               : MIT
Source Database       : grimmdb

Target Server Type    : MYSQL
Target Server Version : 50734
File Encoding         : 65001

Date: 2021-09-30 06:51:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for activity
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '活动表主键ID，用于索引,系统内部可见，数据库自动从1开始自增',
  `title` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '活动标题,发布活动时输入',
  `start_time` datetime NOT NULL COMMENT '活动开始时间,发布活动时输入',
  `location` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '活动地点,发布活动时输入',
  `location_latitude` decimal(9,6) DEFAULT NULL COMMENT '活动地点纬度',
  `location_longitude` decimal(9,6) DEFAULT NULL COMMENT '活动地点经度',
  `end_time` datetime DEFAULT NULL COMMENT '活动结束时间,发布活动时输入，可选',
  `content` varchar(4000) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '活动内容,发布活动时输入',
  `notice` varchar(4000) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '活动注意事项，发布活动时输入，可选',
  `others` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '无' COMMENT '活动其他相关内容，发布活动时输入',
  `admin_raiser` int(11) DEFAULT NULL COMMENT '活动创建者，如果是管理员创建则使用该域，创建活动项时系统自动设置',
  `user_raiser` varchar(28) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '活动创建者，如果是视障人士/志愿者用户则使用该域，创建活动项时系统自动设置',
  `approver` int(11) DEFAULT NULL COMMENT '活动审批者,管理员审批活动时更新',
  `assignee` varchar(28) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '活动领队/负责人,待定',
  `published` int(11) NOT NULL DEFAULT '0' COMMENT '活动审核发布标志位, 0=未审核，1=已审核,管理员审核活动时更新',
  `tag_ids` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '活动分类标签,管理员审核活动时更新',
  `volunteer_capacity` int(11) DEFAULT '0' COMMENT '所需志愿者人数',
  `vision_impaired_capacity` int(11) DEFAULT '0' COMMENT '活动可容纳最大视障者人数',
  `volunteer_job_title` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '对应发布新活动时表单上的岗位名称',
  `volunteer_job_content` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '对应发布新活动时表单上的岗位人数',
  `activity_fee` int(11) DEFAULT '0' COMMENT '活动费用',
  `sign_in_radius` int(11) DEFAULT NULL COMMENT '签到半径，单位公里',
  `sign_in_token` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '签到口令',
  `theme_pic_name` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '活动主题图片, 保存路径为/static/activity_theme_picture/*',
  PRIMARY KEY (`id`),
  KEY `admin_raiser` (`admin_raiser`),
  KEY `approver` (`approver`),
  KEY `assignee` (`assignee`),
  KEY `user_raiser` (`user_raiser`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`admin_raiser`) REFERENCES `admin` (`id`),
  CONSTRAINT `activity_ibfk_2` FOREIGN KEY (`approver`) REFERENCES `admin` (`id`),
  CONSTRAINT `activity_ibfk_3` FOREIGN KEY (`assignee`) REFERENCES `user` (`openid`),
  CONSTRAINT `activity_ibfk_4` FOREIGN KEY (`user_raiser`) REFERENCES `user` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of activity
-- ----------------------------

-- ----------------------------
-- Table structure for activity_participant
-- ----------------------------
DROP TABLE IF EXISTS `activity_participant`;
CREATE TABLE `activity_participant` (
  `activity_id` bigint(20) NOT NULL COMMENT '引用活动ID，关联活动表，进入详情页中的数据库表',
  `participant_openid` varchar(28) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '参加活动的志愿者或者视障人士ID',
  `interested` int(11) DEFAULT '0' COMMENT '是否喜欢，将活动标志为喜欢',
  `share` int(11) DEFAULT '0' COMMENT '分享的次数，一个活动可能会有多次的分享',
  `thumbs_up` int(11) DEFAULT '0' COMMENT '是否点赞，默认值为0',
  `certificated` int(11) DEFAULT NULL COMMENT '是否已经获得过证书，0=未获得，1=已获得',
  `certificate_date` datetime DEFAULT NULL COMMENT '获得证书的日期',
  `paper_certificate` int(11) DEFAULT NULL COMMENT '是否需要纸质证书，0=不需要，1=需要',
  `current_state` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态：Registered, signed_up, signed_off',
  `signup_time` datetime DEFAULT NULL COMMENT '签到时间',
  `signup_latitude` decimal(9,6) DEFAULT NULL COMMENT '签到经纬度-纬度',
  `signup_longitude` decimal(9,6) DEFAULT NULL COMMENT '签到经纬度-经度',
  `signoff_time` datetime DEFAULT NULL COMMENT '签退时间',
  `signoff_latitude` decimal(9,6) DEFAULT NULL COMMENT '签退经纬度-纬度',
  `signoff_longitude` decimal(9,6) DEFAULT NULL COMMENT '签退经纬度-经度',
  PRIMARY KEY (`activity_id`,`participant_openid`),
  KEY `participant_openid` (`participant_openid`),
  CONSTRAINT `activity_participant_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`id`),
  CONSTRAINT `activity_participant_ibfk_2` FOREIGN KEY (`participant_openid`) REFERENCES `user` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of activity_participant
-- ----------------------------

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration_date` datetime NOT NULL COMMENT '管理员账户创建日期,创建新管理员时自动生成',
  `password` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '管理员账户密码哈希串,创建管理员输入密码或管理员更新密码时自动生成',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '管理员姓名,由`root`用户或管理员更新信息时输入',
  `email` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '管理员账户邮箱地址, 创建管理员账户时输入，验证完成之后即为管理员登录账户名',
  `email_verified` int(11) DEFAULT '0' COMMENT '邮箱验证标识位，0=未验证，1=已验证, 新用户在邮件中点击确认认证后设置',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', '2021-09-30 00:00:00', '$2a$05$72h7.uh3480FFuHpGM37me5m.pHd4sLJJoM/qTnwnt2iAB.R11Wvm', 'root', 'no.reply@rp-i.org', '1');

-- ----------------------------
-- Table structure for pickup_impaired
-- ----------------------------
DROP TABLE IF EXISTS `pickup_impaired`;
CREATE TABLE `pickup_impaired` (
  `openid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `activity_id` int(11) NOT NULL COMMENT '活动ID',
  `name` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `id_no` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号码（18位）',
  `impaired_no` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '残疾证编号',
  `pickup_addr` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '接送的起始位置',
  `emergency_contact` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '紧急联系人电话',
  `pickup_method` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '该视障人士被接送的方式',
  `pickup_volunteer_openid` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '该视障人士被接送的志愿者用户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`openid`,`activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of pickup_impaired
-- ----------------------------

-- ----------------------------
-- Table structure for pickup_volunteer
-- ----------------------------
DROP TABLE IF EXISTS `pickup_volunteer`;
CREATE TABLE `pickup_volunteer` (
  `openid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `activity_id` int(11) NOT NULL COMMENT '活动ID',
  `name` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `id_no` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号码',
  `pickup_addr` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '志愿者所在的区域，系统会根据志愿者所在区域就近安排',
  `provide_service` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支援者登记可以提供的志愿者服务（如接视障人士参加活动、送视障人士回家等等），含具体可提供的接送方式',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`openid`,`activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of pickup_volunteer
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `openid` varchar(28) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户表主键值，用于索引，字串由微信生成，对于同一小程序，不同微信用户的openid不相同',
  `registration_date` datetime NOT NULL COMMENT '用户账户申请日期,新用户申请账户时生成',
  `role` int(11) NOT NULL DEFAULT '0' COMMENT '用户类型, 0=志愿者, 1=视障人士,新用户申请账户时设定',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户姓名,用户申请账户时输入，可更新',
  `real_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户真实姓名,用户申请证书时输入，可更新',
  `id_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证件类型：身份证；护照；驾驶证等,用户申请证书时输入，可更新',
  `idcard` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户18位身份证号,用户申请账户时输入，可选',
  `idcard_verified` int(11) DEFAULT '0' COMMENT '身份证号验证标识位，0=未验证，1=已验证,待引用',
  `disabled_id` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '视障人士残疾人证号,视障人士申请账户时输入',
  `disabled_id_verified` int(11) DEFAULT '0' COMMENT '残疾人证号验证标识位，0=未验证，1=已验证,待引用',
  `phone` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户联系电话,用户申请账户时输入，可更新',
  `phone_verified` int(11) NOT NULL DEFAULT '0' COMMENT '联系电话验证标识位，0=未验证，1=已验证,用户申请账户时需先认证联系电话',
  `email` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户邮箱',
  `email_verified` int(11) DEFAULT '0' COMMENT '用户邮箱验证标识位，0=未验证，1=已验',
  `contact` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户备用联系电话,用户申请账户时输入，可选，可更新',
  `gender` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '无' COMMENT '用户性别，"男"或者"女",用户申请账户时输入，可更新',
  `birth` datetime NOT NULL COMMENT '用户生日,用户申请账户时输入，可更新',
  `address` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT '无' COMMENT '用户联系地址,用户申请账户时输入，可更新',
  `emergent_contact` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '视障人士紧急联系人姓名,视障人士申请账户时输入，可更新',
  `emergent_contact_phone` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '视障人士紧急联系人联系电话,视障人士申请账户时输入，可更新',
  `activities_joined` int(11) NOT NULL DEFAULT '0' COMMENT '微信端显示活动参加次数，以及根据次数计算参加时长,待定',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '无' COMMENT '用户备注,用户申请账户时输入',
  `audit_status` int(11) NOT NULL DEFAULT '0' COMMENT '用户注册申请的审核状态,0=进行中, 1=已通过, -1=被拒绝,2=导入数据,管理员审核注册用户时更新',
  `push_status` int(11) NOT NULL DEFAULT '0' COMMENT '???',
  `recipient_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证书收件人姓名,用户申请证书时输入，可更新',
  `recipient_address` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证书收件人地址,用户申请账户时输入，可更新',
  `recipient_phone` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证书收件人电话,用户申请账户时输入，可更新',
  `avatar_url` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户微信头像地址链接',
  PRIMARY KEY (`openid`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `disabled_id` (`disabled_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `idcard` (`idcard`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
