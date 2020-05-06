// pages/register/userlogin.js

const app = getApp()

Page({

  /**
   * Page initial data
   */
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    // 查看是否授权
    wx.getSetting({
      success(res) {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称
          wx.getUserInfo({
            success: function (res) {
              app.globalData.userInfo = res.userInfo;
              console.log(res.userInfo)
            }
          })
        }
      }
    })
    // this.checkJumpToRegisterPage()    
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

  },

  checkJumpToRegisterPage : function() {
    if (this.data.hasUserInfo) {
      wx.navigateTo({
        url: '../register/register',
      })
    }
  },

  jumpToPersonalPage: function() {
    wx.switchTab({
      url: '../personal/personal',
    })
  },

  getUserInfo: function (e) {
    console.log(e)
    console.log(app.globalData.userInfo)
    if(e.detail.userInfo){
      this.setData({
        userInfo: e.detail.userInfo,
        hasUserInfo: true
      })
      app.globalData.userInfo = e.detail.userInfo
      app.globalData.isAuthorized = true;
    }
    wx.navigateBack({
      delta: 1,
    })
    // this.jumpToPersonalPage()
    // this.checkJumpToRegisterPage()
  },

  refuseGetUserInfo: function(){
    wx.showModal({
      title: '拒绝授权',
      content: '无法注册或登陆',
      showCancel: false,
      confirmText: '确定',
      success: function(res) {
        wx.switchTab({
          url: '../home/home',
        });
      }
    })
  }
})