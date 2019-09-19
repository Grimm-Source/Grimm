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
    userInfo: null,
    userInfoList: [
      {
        label: '参加过的活动',
        icon: '../../images/check-circle.png',
        action: ''
      },
      {
        label: '即将参加的活动',
        icon: '../../images/smile.png',
        action: ''
      },
      {
        label: '更新个人信息',
        icon: '../../images/setting.png',
        action: 'updateProfile'
      },
      {
        label: '常见问题',
        icon: '../../images/bulb.png',
        action: ''
      }
    ]
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function () {
    const that = this;
    wx.login({
      success: res => {
        console.log(res.code)
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: apiUrl + 'jscode2session?js_code=' + res.code,
          success: function (res) {
            wx.setStorageSync('openid', res.data.openid)
            console.log('****res:', res)// 服务器回包信息
            if (res.data.is_register) {
              wx.setStorageSync('is_register', true)
              return getProfile(data => {
                that.getInfoSetting(data)
              }, (err) => {
                console.log(err)
              })
            }
          }
        })        
      }
    })
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
    const is_register = wx.getStorageSync('is_register') || false
    if(is_register){
      return getProfile(data => {
        this.getInfoSetting(data)
      }, (err) => {
        console.log(err)
      })
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

  getInfoSetting: function(data){
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              app.globalData.userInfo = res.userInfo
              this.setData({
                userInfo: data,
                avatarUrl: res.userInfo.avatarUrl
              })

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },

  register: function(){
    wx.navigateTo({
      url: '/pages/authorize/authorize',
    })
  },

  updateProfile: function(){
    wx.navigateTo({
      url: '/pages/profile/profile',
    })
  }
})