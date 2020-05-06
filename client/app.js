//app.js
const {getRegisterStatus} = require('utils/requestUtil.js');
App({
  globalData: {
    userInfo: null,
    isAuthorized: false,
    isRegistered: false
  },
  
  onLaunch: function () {
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        const token = res.code;
        this.globalData.token = token;

        wx.getSetting({
          success: res => {
            if (res.authSetting['scope.userInfo']) {
              // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
              wx.getUserInfo({
                lang: "zh_CN",
                success: res => {
                  // 可以将 res 发送给后台解码出 unionId
                  this.globalData.userInfo = res.userInfo;
                  this.globalData.isAuthorized = true;

                  // 检查是否已注册
                  getRegisterStatus(token, function(res){
                    if(!res.openid){
                      return;
                    }
                    wx.setStorageSync('openid', res.openid);
                    wx.setStorageSync('isRegistered', !!res.isRegistered);
                    wx.setStorageSync('auditStatus', res.auditStatus || "pending");
                    this.globalData.isRegistered = !!res.isRegistered;
                    // this.globalData.userInfo = res.userInfo;
                });    
    
                  // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                  // 所以此处加入 callback 以防止这种情况
                  if (this.userInfoReadyCallback) {
                    this.userInfoReadyCallback(res)
                  }
                }
              })
            }
          }
        });   
      }
    });

    //
  }
})