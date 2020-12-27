var app = getApp();
const {getRegisterStatus, getPhoneNumber} = require('../../utils/requestUtil.js');

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
    isRegistered: app.globalData.isRegistered,
    isAuthorized: app.globalData.isAuthorized,
    isVolunteer: app.globalData.isVolunteer,
    progress_attendMinutes: '0 分钟',  
    progress_attendTimes: '0 次活动',  
    personalInfoList: [
      {
        label: '我的活动',
        action: 'onMyActivityTap',
        class: 'myActivity'
      },
      {
        label: '已报名活动',
        action: 'onRegisteredTap',
        class: 'registered'
      },
      {
        label: '感兴趣的活动',
        action: 'onMyFavoriteTap',
        class: 'myFavorite'
      }
    ]
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    this.setData({
      isAuthorized: app.globalData.isAuthorized,
      isRegistered: app.globalData.isRegistered,
      userInfo: app.globalData.userInfo,
      isVolunteer: app.globalData.isVolunteer
    })
  },

  /**
   * Lifecycle function--Called when page is initially rendered
   */
  onReady: function () {
    this.drawProgressbg(); 
  },

  /**
   * Lifecycle function--Called when page show
   */
  onShow: function () {
    this.setData({
      isAuthorized: app.globalData.isAuthorized,
      isRegistered: app.globalData.isRegistered,
      userInfo: app.globalData.userInfo,
      isVolunteer: app.globalData.isVolunteer
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
    if(!app.globalData.isAuthorized){
      wx.navigateTo({
        url: '/pages/authorize/authorize',
      });
      return;
    }
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
          getPhoneNumber(param, res => {
            if (res.decrypt_data.phoneNumber) {
              wx.navigateTo({
                url: `/pages/register/register?phone=${res.decrypt_data.purePhoneNumber}`,
              })
            } else {
              // TODO 如果获取到微信绑定的手机号则不再发短信验证手机号，原先这部分逻辑是把注册和登录分开，登录时必须验证手机号，现在是整合成自动登录，后续可以再详细分开
              console.log("get no phone number")
              wx.navigateTo({
                url: '/pages/login/login',
              });
            }
          })
        }
      })
    }
  },

  drawProgressbg: function(){
    var ctx1 = wx.createCanvasContext('canvasProgressbg1',this)
    ctx1.setLineWidth(2);
    ctx1.setStrokeStyle('#6E6E6E');
    ctx1.setLineCap('round');
    ctx1.beginPath();
    ctx1.arc(55, 55, 50, 0, 2 * Math.PI, false);
    
    ctx1.stroke();
    ctx1.draw();

    var ctx2 = wx.createCanvasContext('canvasProgressbg2',this)
    ctx2.setLineWidth(2);
    ctx2.setStrokeStyle('#6E6E6E');
    ctx2.setLineCap('round');
    ctx2.beginPath();
    ctx2.arc(55, 55, 50, 0, 2 * Math.PI, false);
    
    ctx2.stroke();
    ctx2.draw();
  },

  onMyActivityTap: function () {
    wx.navigateTo({
      url: '/pages/myActivity/myActivity?selectedIdx=0',
    });
  },

  onRegisteredTap: function () {
    wx.navigateTo({
      url: '/pages/myActivity/myActivity?selectedIdx=1',
    });
  },
  
  onMyFavoriteTap: function () {
    wx.navigateTo({
      url: '/pages/myActivity/myActivity?selectedIdx=2',
    });
  },

  onEditTap: function () {
    if(!this.data.isRegistered){
      wx.showToast({
        title: '请先注册',
        icon: 'none', //error
        duration: 2000
      });
      return;
    }
    wx.navigateTo({
      url: '/pages/personalProfile/personalProfile',
    })
  }

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
})