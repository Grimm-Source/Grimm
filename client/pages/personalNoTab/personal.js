var app = getApp();
const {getRegisterStatus} = require('../../utils/requestUtil.js');

Page({

  /**
   * Page initial data
   */
  data: {
    setting_list: [
      {
        icon: '../../images/scan.png',
        action: 'scanCode',
        label:'扫一扫'
      },
      // {
      //   icon: '../../images/set.png',
      //   action: 'settingProfile'
      // }
    ],
    avatarUrl: '../../images/avatar.jpg',
    userInfo: null,
    isRegistered: false,
    isAuthorized: false,
    personalInfoList: [
      {
        label: '我的活动',
        action: 'tapMyActivity',
        class: 'myActivity'
      },
      {
        label: '已报名活动',
        action: '',
        class: 'registered'
      },
      {
        label: '感兴趣的活动',
        action: '',
        class: 'myFavorite'
      },
      {
        label: '参加过的活动',
        action: '',
        class: 'haveEntered'
      }
    ]
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    wx.setNavigationBarTitle({
      title: '个人中心'
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
    this.setData({
      isAuthorized: app.globalData.isAuthorized,
      isRegistered: app.globalData.isRegistered,
      userInfo: app.globalData.userInfo
    })
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

  // onTapRegisteredActivities: function(){
  //   wx.navigateTo({
  //     url: '/pages/activityList/activityList?type=REGISTERED',
  //   });
  // },

  // getInfoSetting: function(){
  //   wx.getSetting({
  //     success: res => {
  //       if (res.authSetting['scope.userInfo']) {
  //         // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
  //         wx.getUserInfo({
  //           success: res => {
  //             // 可以将 res 发送给后台解码出 unionId
  //             app.globalData.userInfo = res.userInfo
  //             this.setData({
  //               userInfo: res.userInfo,
  //               avatarUrl: res.userInfo.avatarUrl
  //             })

  //             // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
  //             // 所以此处加入 callback 以防止这种情况
  //             if (this.userInfoReadyCallback) {
  //               this.userInfoReadyCallback(res)
  //             }
  //           }
  //         })
  //       }
  //     }
  //   });
      
  // },

  onAuthorizeTap: function(){
    wx.navigateTo({
      url: '/pages/authorize/authorize',
    });
  },

  onRegisterTap: function(e){
    if (e.detail.iv && e.detail.encryptedData) {
      wx.login({
        success: res => {
          const param = {
            js_code: res.code,
            encryptedData: e.detail.encryptedData,
            iv: e.detail.iv
          };
          // getPhoneNumber(param, res => {
          //   wx.navigateTo({
          //     url: `/pages/register/register?phone=${res.decrypt_data.purePhoneNumber}`,
          //   })
          // })
          wx.navigateTo({
            url: `/pages/register/register?phone=18201798201`,
          })
        }
      })
    }
  },

  // updateProfile: function(){
  //   if(this.data.isRegistered && this.data.auditStatus === "pending"){
  //     wx.showToast({
  //       title: '个人信息正在审核，无法更新',
  //       icon: 'none', //error
  //       duration: 2000
  //     });
  //     return;
  //   }
  //   if(!this.data.isRegistered){
  //     wx.showToast({
  //       title: '请先注册',
  //       icon: 'none', //error
  //       duration: 2000
  //     });
  //     return;
  //   }
  //   wx.navigateTo({
  //     url: '/pages/profile/profile',
  //   })
  // }
  tapMyActivity: function(){
    if(this.data.isAuthorized){
      wx.navigateTo({
        url: `/pages/myActivity/myActivity`,
      })
    }else{
      wx.showToast({
        title: '请先授权',
        icon: 'none', //error
        duration: 2000
      });
      return;
    }
  }
})