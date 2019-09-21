/*
 * create the mainInfo Table for user
 */
CREATE TABLE mainInfo (
        openid           varchar(35) NOT NULL,
        birthdate        date NOT NULL,
        usercomment      varchar(100),
        disabledID       varchar(20),
        emergencyPerson  varchar(10),
        emergencyTel     char(11),
        gender           varchar(5) NOT NULL,
        idcard           char(18) NOT NULL,
        linkaddress      varchar(80) NOT NULL,
        linktel          char(11) NOT NULL,
        name             varchar(10) NOT NULL,
        role             varchar(10) NOT NULL,
        tel              varchar(11) NOT NULL,
        PRIMARY KEY(openid)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
