// pages/certificate/applyList.js
const { getCertificatectivity } = require('../../utils/requestUtil.js');

/**
 * 
 * 
 * 
    activity_id                 BIGINT,
    participant_openid          CHAR(28)            NOT NULL, 
    interested                  TINYINT             DEFAULT 0,
    share                       INT                 DEFAULT 0,
    thumbs_up                   TINYINT             DEFAULT 0,
    certificated                TINYINT,
    certificate_date            DATE,
    paper_certificate           TINYINT,
 */

Page({

  /**
   * 页面的初始数据
   */
  data: {
    activityList: [{activity_id: 1}, {activity_id: 2}, {activity_id: 3}, {activity_id: 4}, {activity_id: 5}, {activity_id: 6}, {activity_id: 7}],
    checkList:[],
    participant_openid: '',
    isLoading: false,
    submitDisabled: false
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    getCertificatectivity({},
      (res)=>{
        this.setData({
          activityList: res.activities,
          participant_openid: res.participant_openid
        })
    },
    (fail)=>{
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
  getActivitData: function(){

  },
  /**
   * 选择活动
   */
  onActCheck: function(e){
    this.setData({
      checkList: e.detail.value,
      submitDisabled: false
    }) 
  },

  onSubmit: function(){

  }
})