/*
 * tianyxu 2019-Sep-10 according discussion with xiaoting get this table
 * mysql -uroot -p123Xty1. -Dgrimm<./example.sql
 * or can use source in the mysql cli
 * create the admin Table for admin user
 */
CREATE TABLE admin (
        id               integer     NOT NULL AUTO_INCREMENT,
        email            varchar(40) NOT NULL,
        password         varchar(20) NOT NULL,
        admintype        varchar(10) NOT NULL,
        PRIMARY KEY(id)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO admin (id, email, password, admintype) VALUES (520, "grimm@cisco.com", "123", "root");
