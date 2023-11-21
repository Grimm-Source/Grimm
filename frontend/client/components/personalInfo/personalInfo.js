// components/personalInfo.js
var app = getApp();
const {getRegisterStatus, getPhoneNumber} = require('../../utils/requestUtil.js');

Component({
  /**
   * Component properties
   */
  properties: {

  },

  /**
   * Component initial data
   */
  data: {
    setting_list: [
      {
        icon: '../../images/scan.png',
        action: 'scanCode',
        label:'扫一扫'
      },
    ],
    avatarUrl: '../../images/avatar.jpg',
    userInfo: null,
    isRegistered: app.globalData.isRegistered,
    isAuthorized: app.globalData.isAuthorized,
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

  pageLifetimes: {

    show: function() {
      this.drawProgressbg(); 
      this.setData({
        isAuthorized: app.globalData.isAuthorized,
        isRegistered: app.globalData.isRegistered,
        userInfo: app.globalData.userInfo
      })
    }
  },

  /**
   * Component methods
   */
  methods: {
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
            getPhoneNumber(param, res => {
              wx.navigateTo({
                url: `/pages/register/register?phone=${res.decrypt_data.purePhoneNumber}`,
              })
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
      // if(!this.data.isRegistered){
      //   wx.showToast({
      //     title: '请先注册',
      //     icon: 'none', //error
      //     duration: 2000
      //   });
      //   return;
      // }
      wx.navigateTo({
        url: '/pages/personalProfile/personalProfile',
      })
    }
  }
})
