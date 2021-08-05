// pages/certificate/applyList.js
const {
  getCertificatectivity
} = require('../../utils/requestUtil.js');

/**
 *
 *
 *
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
 */

Page({

  /**
   * 页面的初始数据
   */
  data: {
    activityList: [],
    checkList: [],
    participant_openid: '',
    isLoading: false,
    submitDisabled: false,
    isEmpty: false,
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    getCertificatectivity({},
      (res) => {
        const activities = res.activities.filter((item)=>{
          return !item.published || +item.published === 0
         }).map(((item)=>{
          item.start_time = item.start_time.replace('T', ' ');
          return item;
        }))
        this.setData({
          activityList: activities.concat(activities),
          participant_openid: res.participant_openid,
          isEmpty: !activities || activities.length === 0
        })
      },
      (fail) => {
        wx.showToast({
          title: fail || '活动获取失败',
          icon: 'none', //error
          duration: 2000
        });
      }
    );
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  /**
   * 获取可开具证明的活动
   */
  getActivitData: function () {

  },
  /**
   * 选择活动
   */
  onActCheck: function (e) {
    this.setData({
      checkList: e.detail.value,
      submitDisabled: false
    })
  },

  onSubmit: function () {
    const {checkList} = this.data;
    if(!checkList || checkList.length < 1){
      wx.showToast({
        title: '请选择活动',
        icon: 'error', //error
        duration: 2000
      });
    }else{
      wx.setStorageSync('cer_acc_list', checkList);
      wx.setStorageSync('participant_openid', this.data.participant_openid);
      wx.navigateTo({
        url: '/pages/certificate/applyForm',
      });
    }
  }
})
