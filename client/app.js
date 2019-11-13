//app.js
const apiUrl = require('./config.js').apiUrl
const {getRegisterStatus} = require('utils/requestUtil.js');
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        getRegisterStatus(res.code, function(res){
            if(!res.openid){
              return;
            }
            wx.setStorageSync('openid', res.openid);
            wx.setStorageSync('isRegistered', !!res.isRegistered);
            wx.setStorageSync('auditStatus', res.auditStatus || "pending");
        });       
      }
    });
  },
  globalData: {
    userInfo: null
  }
})