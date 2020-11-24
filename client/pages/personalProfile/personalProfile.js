// pages/personalProfile/personalProfile.js
var app = getApp();
const { getProfile, updateProfile } = require('../../utils/requestUtil.js');
Page({

  /**
   * Page initial data
   */
  data: {
    genders: ['男', '女'],
    roleShow: ['视障者','志愿者'],
    roleShowIndex: 0, //0:impaired 1:volunteer
    avatarUrl: '../../images/avatar.jpg',
    userInfo: {
      tel: '',
      name: '',
      genderIndex: 0,
      gender: '',
      birthDate: '',
      linkaddress: '',
      role:'',
      idcard: '',
      disabledID: '',
      email: ''
    }
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
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
    },(err) => {
      wx.showModal({
        title: '提示',
        content: err,
        showCancel: false,
        success () {
          // wx.switchTab({
          //   url: '../home/home',
          // });
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

  bindRoleChanged:function (e) {
    this.setData({
      'userInfo.role': e.detail.value == 0 ? 'impaired' : 'volunteer',
      roleShowIndex: e.detail.value
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

  bindIdCardChange: function (e) {
    this.setData({
      'userInfo.idcard' : e.detail.value
    })
  },

  bindDisabledIDChange: function (e) {
    this.setData({
      'userInfo.disabledID' : e.detail.value
    })
  },

  bindEmailChange: function (e) {
    this.setData({
      'userInfo.email' : e.detail.value
    })
  },

  updateProfile: function(){
    if (this.data.userInfo.role == 'impaired' && !this.data.userInfo.disabledID) {
      wx.showModal({
        title: '提示',
        content: '请填写残疾证号码',
        showCancel: false,
      });
      return;
    }
    if (!this.data.userInfo.name) {
      wx.showModal({
        title: '提示',
        content: '请填写真实姓名',
        showCancel: false,
      })
      return;
    }
    var idReg = /^(([1][1-5])|([2][1-3])|([3][1-7])|([4][1-6])|([5][0-4])|([6][1-5])|([7][1])|([8][1-2]))\d{4}(([1][9]\d{2})|([2]\d{3}))(([0][1-9])|([1][0-2]))(([0][1-9])|([1-2][0-9])|([3][0-1]))\d{3}[0-9xX]$/;
    var passportReg = /^([a-zA-z]|[0-9]){5,17}$/;
    if (!idReg.test(this.data.userInfo.idcard) && !passportReg.test(this.data.userInfo.idcard)) {
      wx.showModal({
        title: '提示',
        content: '请输入身份证号/护照号',
        showCancel: false,
      })
      return;
    }
    if (!this.data.userInfo.email) {
      wx.showModal({
        title: '提示',
        content: '请输入邮箱',
        showCancel: false,
      })
      return;
    }
    return updateProfile(this.data.userInfo, (res)=>{
      //console.log(this.data);
      app.globalData.isVolunteer = this.data.userInfo.role == 'volunteer' ? true : false;
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