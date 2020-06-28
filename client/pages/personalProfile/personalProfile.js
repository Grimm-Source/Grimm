// pages/personalProfile/personalProfile.js
var app = getApp();
const {getProfile} = require('../../utils/requestUtil.js');
Page({

  /**
   * Page initial data
   */
  data: {
    phone: '',
    name: '',
    genders: ['男', '女'],
    genderIndex: 0,
    birthday: '',
    region: [],
    userInfo: null
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    console.log('kk')
    this.setData({
      userInfo: app.globalData.userInfo
    })
    return getProfile((data) => {
      this.setData({
        userInfo: data,
        userInfoSource: Object.assign({}, data)
      });
    },(err) => {
      wx.showModal({
        title: '提示',
        content: err,
        showCancel: false,
        success () {
          wx.switchTab({
            url: '../home/home',
          });
        }
      });     
    });
  },

  /**
   * Lifecycle function--Called when page is initially rendered
   */
  onReady: function () {

  },

  /**
   * Lifecycle function--Called when page show
   */
  onShow: function () {

  },

  /**
   * Lifecycle function--Called when page hide
   */
  onHide: function () {

  },

  /**
   * Lifecycle function--Called when page unload
   */
  onUnload: function () {

  },

  /**
   * Page event handler function--Called when user drop down
   */
  onPullDownRefresh: function () {

  },

  /**
   * Called when page reach bottom
   */
  onReachBottom: function () {

  },

  /**
   * Called when user click on the top right corner to share
   */
  onShareAppMessage: function () {

  }
})