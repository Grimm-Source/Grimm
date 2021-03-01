// pages/register/userlogin.js
const { getRegisterStatus } = require('../../utils/requestUtil.js');
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
    if(options.redirectPage){
      const redirectPage = options.redirectPage;
      const key = options.key;
      const value = options.value;
      const redirectUrl = key?`../${redirectPage}/${redirectPage}?${key}=${value}`:`../${redirectPage}/${redirectPage}`;
      this.setData({
        redirectUrl
      });
    }


    // 查看是否授权
    wx.getSetting({
      success(res) {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称
          wx.getUserInfo({
            success: function (res) {
              app.globalData.userInfo = res.userInfo;
              console.log(res.userInfo);
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
    if(app.globalData.isAuthorized){
      wx.switchTab({
        url: '../home/home',
      });
    }
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
      // 检查是否授权
      wx.login({
        success: res => {
          getRegisterStatus(res.code, function(res){
            console.log("resopenid")
            console.log(res.openid)
            if(!res.openid){
              return;
            }
            app.globalData.auditStatus = res.auditStatus || "pending";
            app.globalData.isRegistered = res.isRegistered;
            app.globalData.isVolunteer = res.role == "volunteer";
            wx.setStorageSync("openid",res.openid)
          }).then(res => {
            console.log("global register")
            console.log(app.globalData.isRegistered)
            wx.switchTab({
              url: '../home/home',
            })
          });
        },
      })
      app.globalData.userInfo = e.detail.userInfo
      app.globalData.isAuthorized = true;
    }
    if(this.data.redirectUrl){
      wx.navigateTo({
        url: this.data.redirectUrl,
      })
    }else{
      this.jumpToPersonalPage()
    }
    
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