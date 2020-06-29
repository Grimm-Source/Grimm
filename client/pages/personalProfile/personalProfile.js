// pages/personalProfile/personalProfile.js
var app = getApp();
const { getProfile, updateProfile } = require('../../utils/requestUtil.js');
Page({

  /**
   * Page initial data
   */
  data: {
    genders: ['男', '女'],
    avatarUrl: '../../images/avatar.jpg',
    userInfo: {
      tel: '',
      name: '',
      genderIndex: 0,
      gender: '',
      birthDate: '',
      linkaddress: ''
    }
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    console.log('kk')
    this.setData({
      avatarUrl: app.globalData.userInfo.avatarUrl
    })
    return getProfile((data) => {
      const defaultUserInfo = data;
      // defaultUserInfo.linkaddress = ['北京市', '北京市', '东城区'];
      // console.log(addressArr)
      this.setData({
        userInfo: defaultUserInfo,
        userInfoSource: Object.assign({}, data)
      });
      console.log(this.data.userInfo)
    },(err) => {
      wx.showModal({
        title: '提示',
        content: err,
        showCancel: false,
        success () {
          wx.switchTab({
            url: '../home/home',
          });
        }
      });     
    });
  },

  bindNameChange: function (e) {
    this.setData({
      'userInfo.name' : e.detail.value
    })
  },

  bindGenderChange: function (e) {
    this.setData({
      'userInfo.gender': e.detail.value == 0 ? '男' : '女'
    })
  },

  bindBirthdayChange: function(e) {
    this.setData({
      'userInfo.birthDate': e.detail.value
    })
  },

  bindRegionChange: function (e) {
    this.setData({
      'userInfo.linkaddress': e.detail.value.join('')
    })
  },

  updateProfile: function(){
    return updateProfile(this.data.userInfo, (res)=>{
      wx.showToast({
        title: '已更新',
        icon: 'success',
        duration: 300
      });
      wx.switchTab({
        url: '../personal/personal',
      });
    },(err)=>{
      wx.showModal({
        showCancel: false,
        title: '更新失败',
        content: err || "网络失败，请稍候再试"
      });  
    });
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

  }
})