//app.js
const apiUrl = require('./config.js').apiUrl
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
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
              wx.setStorageSync('is_register', false)
            }else{
              wx.setStorageSync('is_register', true)
            }
          }
        })        
      }
    })
  },
  globalData: {
    userInfo: null
  }
})