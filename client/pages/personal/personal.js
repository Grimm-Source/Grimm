// pages/personal2/personal2.js
var app = getApp();

Page({

  /**
   * Page initial data
   */
  data: {
    setting_list: [
      {
        icon: '../../images/scan.png',
        action: 'scanCode'
      },
      {
        icon: '../../images/set.png',
        action: 'settingProfile'
      }
    ],
    avatarUrl: '../../images/avatar.jpg',
    userInfo: null,
    activity_list: [
      {
        icon: '../../images/order.png',
        label: '已预约'
      },
      {
        icon: '../../images/signature.png',
        label: '已签到'
      },
      {
        icon: '../../images/no_signature.png',
        label: '未签到'
      }
    ],
    personalInfoList: [
      {
        label: '我的活动列表',
        action: ''
      },
      {
        label: '我的通知',
        action: ''
      },
      {
        label: '更新个人信息',
        action: 'updateProfile'
      },
      {
        label: '常见问题',
        action: ''
      },
      {
        label: '用户反馈',
        action: ''
      }
    ]
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {

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
    this.setData({
      isRegistered: wx.getStorageSync('isRegistered') || false,
      auditStatus: wx.getStorageSync('auditStatus') || "pending"
    });
    this.getInfoSetting(); 
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

  getInfoSetting: function(){
    if(this.data.isRegistered){
      wx.getSetting({
        success: res => {
          if (res.authSetting['scope.userInfo']) {
            // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
            wx.getUserInfo({
              success: res => {
                // 可以将 res 发送给后台解码出 unionId
                app.globalData.userInfo = res.userInfo
                this.setData({
                  userInfo: res.userInfo,
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
    }
  },

  register: function(){
    wx.navigateTo({
      url: '/pages/authorize/authorize',
    })
  },

  updateProfile: function(){
    if(this.data.isRegistered && this.data.auditStatus === "pending"){
      wx.showToast({
        title: '个人信息正在审核，无法更新',
        icon: 'none', //error
        duration: 2000
      });
      return;
    }
    if(!this.data.isRegistered){
      wx.showToast({
        title: '请先注册',
        icon: 'none', //error
        duration: 2000
      });
      return;
    }
    wx.navigateTo({
      url: '/pages/profile/profile',
    })
  }
})