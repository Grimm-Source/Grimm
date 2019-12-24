//app.js
const {getRegisterStatus} = require('utils/requestUtil.js');
App({
  onLaunch: function () {
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