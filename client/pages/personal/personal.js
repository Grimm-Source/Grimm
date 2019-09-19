const apiUrl = require('../../config.js').apiUrl
const {getProfile} = require('../../utils/requestUtil.js');


var app = getApp();

// pages/personal/personal.js
Page({

  /**
   * Page initial data
   */
  data: {
    avatarUrl: '../../images/defaultAvatar.jpeg',
    userInfo: null
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    return getProfile((data) => {
      this.setData({
        userInfo: data
      });
    },(err) => {
      console.log(err)   
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

  },

  login_register: function(){
    wx.login({
      success: res => {
        console.log(res.code)
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: apiUrl + 'jscode2session?js_code=' + res.code,
          success: function (res) {
            wx.setStorageSync('openid', res.data.openid)
            console.log('****res:', res)// 服务器回包信息
            if (!res.data.is_register) {
              wx.showModal({
                title: '提示',
                content: '请先注册',
                showCancel: false,
                confirmText: '确定',
                success: function(res) {
                  wx.navigateTo({
                    url: '/pages/authorize/authorize',
                  })
                }
              })
            }else{
              wx.switchTab({
                url: '/pages/home/home'
              })
            }
          }
        })        
      }
    })
  },

  // register: function(){
  //   wx.navigateTo({
  //     url: '/pages/authorize/authorize',
  //   })
  // },

  updateProfile: function(){
    wx.navigateTo({
      url: '/pages/profile/profile',
    })
  }
})