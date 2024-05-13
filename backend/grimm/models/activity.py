from sqlalchemy import func
from sqlalchemy.orm import relationship

from grimm import db

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(60), nullable=False, unique=True, comment='项目名')

class Duty(db.Model):
    __tablename__ = 'duty'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(60), nullable=False, unique=True, comment='活动中担任的职责')
    seq = db.Column(db.Integer, nullable=False, unique=True, comment='导出汇总表时的列顺序，小的数字靠左')

class Gift(db.Model):
    __tablename__ = 'gift'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    seq = db.Column(db.Integer, nullable=False, unique=True, comment='导出汇总表时的列顺序，小的数字靠左')

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='活动表主键ID，用于索引,系统内部可见，数据库自动从1开始自增')
    title = db.Column(db.String(60), nullable=False, comment='活动标题,发布活动时输入')
    start_time = db.Column(db.DateTime, nullable=False, comment='活动开始时间,发布活动时输入')
    location = db.Column(db.String(100), nullable=False, comment='活动地点,发布活动时输入')
    location_latitude = db.Column(db.DECIMAL(9,6), comment='活动地点纬度')
    location_longitude = db.Column(db.DECIMAL(9,6), comment='活动地点经度')
    end_time = db.Column(db.DateTime, comment='活动结束时间,发布活动时输入，可选')
    content = db.Column(db.String(4000), nullable=False, comment='活动内容,发布活动时输入')
    notice = db.Column(db.String(4000), comment='活动注意事项，发布活动时输入，可选')
    others = db.Column(db.String(120), nullable=False, server_default='无', comment='活动其他相关内容，发布活动时输入')
    admin_raiser = db.Column(db.Integer, db.ForeignKey('admin.id'), comment='活动创建者，如果是管理员创建则使用该域，创建活动项时系统自动设置')
    user_raiser = db.Column(db.String(28), db.ForeignKey('user.openid'), comment='活动创建者，如果是视障人士/志愿者用户则使用该域，创建活动项时系统自动设置')
    approver = db.Column(db.Integer, db.ForeignKey('admin.id'), comment='活动审批者,管理员审批活动时更新')
    # assignee = db.Column(db.String(28), db.ForeignKey('user.openid'), comment='活动领队/负责人,待定')
    published = db.Column(db.Integer, nullable=False, server_default='0', comment='活动审核发布标志位, 0=未审核，1=已审核,管理员审核活动时更新')
    tag_ids = db.Column(db.String(120), comment='活动分类标签,管理员审核活动时更新')
    volunteer_capacity = db.Column(db.Integer, server_default='0', comment='所需志愿者人数')
    vision_impaired_capacity = db.Column(db.Integer, server_default='0', comment='活动可容纳最大视障者人数')
    volunteer_job_title = db.Column(db.String(500), comment='对应发布新活动时表单上的岗位名称')
    # TODO Duty?
    volunteer_job_content = db.Column(db.String(100), comment='对应发布新活动时表单上的岗位人数')
    activity_fee = db.Column(db.Integer, server_default='0', comment='活动费用')
    sign_in_radius = db.Column(db.Integer, comment='签到半径，单位公里')
    sign_in_token = db.Column(db.String(10), nullable=False, comment='签到口令')
    theme_pic_name = db.Column(db.String(300), nullable=False, comment='活动主题图片, 保存路径为/static/activity_theme_picture/*')
    project_seq = db.Column(db.Integer, comment='对应项目的活动场次')
    project_id = db.Column(db.BigInteger, db.ForeignKey('project.id'))
    remark = db.Column(db.String(500), comment='备注')

    project = relationship('Project', backref='activities')

    @property
    def volunteers(self):
        return [info.user for info in self.participate_infos if info.user.is_volunteer()]

    @property
    def impaireds(self):
        return [info.user for info in self.participate_infos if info.user.is_impaired()]

    @property
    def children_count(self):
        return len([x for x in self.participate_infos \
                if x.is_child == True])

    @property
    def start_date(self):
        return self.start_time.strftime('%Y-%m-%d')

class ActivityParticipant(db.Model):
    __tablename__ = 'activity_participant'
    activity_id = db.Column(db.BigInteger, db.ForeignKey('activity.id'), primary_key=True, comment='引用活动ID，关联活动表，进入详情页中的数据库表')
    participant_openid = db.Column(db.String(28), db.ForeignKey('user.openid'), primary_key=True, comment='参加活动的志愿者或者视障人士ID')
    interested = db.Column(db.Integer, server_default='0', comment='是否喜欢，将活动标志为喜欢')
    share = db.Column(db.Integer, server_default='0', comment='分享的次数，一个活动可能会有多次的分享')
    thumbs_up = db.Column(db.Integer, server_default='0', comment='是否点赞，默认值为0')
    certificated = db.Column(db.Integer, comment='是否已经获得过证书，0=未获得，1=已获得')
    certificate_date = db.Column(db.DateTime, comment='获得证书的日期')
    paper_certificate = db.Column(db.Integer, comment='是否需要纸质证书，0=不需要，1=需要')
    current_state = db.Column(db.String(10), comment='状态：Registered, signed_up, signed_off')
    sign_method = db.Column(db.String(10), comment='签到方式：token, gps=default')
    signup_time = db.Column(db.DateTime, comment='签到时间')
    signup_latitude = db.Column(db.DECIMAL(9, 6), comment='签到经纬度-纬度')
    signup_longitude = db.Column(db.DECIMAL(9, 6), comment='签到经纬度-经度')
    signoff_time = db.Column(db.DateTime, comment='签退时间')
    signoff_latitude = db.Column(db.DECIMAL(9, 6), comment='签退经纬度-纬度')
    signoff_longitude = db.Column(db.DECIMAL(9, 6), comment='签退经纬度-经度')
    duty_id = db.Column(db.BigInteger, db.ForeignKey('duty.id'))
    is_child = db.Column(db.Boolean, server_default='0', comment='报名人是否是孩子')
    gifts = db.Column(db.JSON, comment='领取物品种类和数量')

    duty = relationship('Duty')
    user = relationship('User', backref='participate_infos')
    activity = relationship('Activity', backref='participate_infos')

    @property
    def duty_name(self):
        return self.duty.name if self.duty else ''

class PickupImpaired(db.Model):
    __tablename__ = 'pickup_impaired'
    openid = db.Column(db.String(64), primary_key=True, comment='用户ID')
    activity_id = db.Column(db.Integer, primary_key=True, comment='活动ID')
    name = db.Column(db.String(32), comment='真实姓名')
    id_no = db.Column(db.String(18), comment='身份证号码（18位）')
    impaired_no = db.Column(db.String(20), comment='残疾证编号')
    pickup_addr = db.Column(db.String(256), comment='接送的起始位置')
    emergency_contact = db.Column(db.String(32), comment='紧急联系人电话')
    pickup_method = db.Column(db.String(32), comment='该视障人士被接送的方式')
    pickup_volunteer_openid = db.Column(db.String(64), comment='该视障人士被接送的志愿者用户ID')
    create_time = db.Column(db.DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')


class PickupVolunteer(db.Model):
    __tablename__ = 'pickup_volunteer'
    openid = db.Column(db.String(64), primary_key=True, comment='用户ID')
    activity_id = db.Column(db.Integer, primary_key=True, comment='活动ID')
    name = db.Column(db.String(32), comment='真实姓名')
    id_no = db.Column(db.String(18), comment='身份证号码')
    pickup_addr = db.Column(db.String(512), comment='志愿者所在的区域，系统会根据志愿者所在区域就近安排')
    provide_service = db.Column(db.String(32), comment='支援者登记可以提供的志愿者服务（如接视障人士参加活动、送视障人士回家等等），含具体可提供的接送方式')
    create_time = db.Column(db.DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
