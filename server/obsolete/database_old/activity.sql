/*
 * tianyxu 2019-Sep-10 according discussion with xiaoting get this table
 * mysql -uroot -p123Xty1. -Dgrimm<./example.sql
 * or can use source in the mysql cli
 * create the admin Table for admin user
 */
CREATE TABLE activity (
        id               integer       NOT NULL AUTO_INCREMENT,
        adminId          integer       NOT NULL,
        title            varchar(100)   NOT NULL,
        location         varchar(100)   NOT NULL,
        activitydate     datetime       NOT NULL,
        duration         varchar(20)   NOT NULL,
        content          varchar(1000) NOT NULL,
        notice           varchar(300),
        others           varchar(100),
        PRIMARY KEY(id),
        FOREIGN KEY(adminId) REFERENCES admin(id)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
