//获取应用实例
const { getActivityList, getActivityTypes, getRegisterStatus } = require('../../utils/requestUtil.js');

const app = getApp()

Page({
  data: {
    activityCategories: [],
    activities:[],
    needShowTabbar: true,
    showTabbarText: "隐藏",
    isAuthorized: false,
    userInfo: null,
    avatarUrl: '../../images/avatar.jpg',
  },
  
  onLoad: function (options) {
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        const token = res.code;
        app.globalData.token = token;

        wx.getSetting({
          success: res => {
            if (res.authSetting['scope.userInfo']) {
              // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
              wx.getUserInfo({
                lang: "zh_CN",
                success: res => {
                  // 可以将 res 发送给后台解码出 unionId
                  app.globalData.userInfo = res.userInfo;
                  app.globalData.isAuthorized = true;
                  this.setData({
                    isAuthorized: app.globalData.isAuthorized,
                    userInfo: app.globalData.userInfo
                  })

                  // 检查是否已注册
                  getRegisterStatus(token, function(res){
                    if(!res.openid){
                      return;
                    }
                    wx.setStorageSync('openid', res.openid);
                    wx.setStorageSync('isRegistered', !!res.isRegistered);
                    wx.setStorageSync('auditStatus', res.auditStatus || "pending");
                    app.globalData.isRegistered = !!res.isRegistered;
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
  },

  onShow: function () {
    this.selectComponent(".home-tips-siwper").getData();
    this.setData({
      isAuthorized: app.globalData.isAuthorized,
      userInfo: app.globalData.userInfo
    })
  },

  toggleTabbar: function() {
    this.setData({
      needShowTabbar: !this.data.needShowTabbar,
      showTabbarText: this.data.needShowTabbar ? "隐藏" : "显示"
    });

    if (!this.data.needShowTabbar) {
      wx.hideTabBar();
    } else {
      wx.showTabBar();
    }
  },

  showPersonInfo: function() {
    wx.navigateTo({
      url: "/pages/personalNoTab/personal",
      fail: function(res) {
        console.log(res);
      }
    });
  },

  scanCode: function(){
    wx.scanCode({
      success: (res) => {
        console.log("扫码结果");
        console.log(res);
      },
      fail: (res) => {
        console.log(res);
      }
    })
  }
  
})
