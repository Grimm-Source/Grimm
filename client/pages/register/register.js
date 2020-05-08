const { register} = require('../../utils/requestUtil.js');
const app = getApp();

Page({
  data: {
    phone: '',
    name: '',
    genders: ['男', '女'],
    roles: ['志愿者', '视障人士'],
    roleIndex: 0,
    genderIndex: 0,
    birthday: '',
    region: []
  },

  onLoad: function (options) {
    this.setData({
      phone: options.phone
    });
  },

  bindNameChange: function (e) {
    this.setData({
      name : e.detail.value
    })
  },

  bindGenderChange: function (e) {
    this.setData({
      genderIndex: e.detail.value
    })
  },

  bindRoleChange: function(e){
    this.setData({
      roleIndex: e.detail.value
    })
  },

  bindBirthdayChange: function(e) {
    this.setData({
      birthday: e.detail.value
    })
  },

  bindRegionChange: function (e) {
    this.setData({
      region: e.detail.value
    })
  },

  onSubmit: function() {
    if (!this.data.name) {
      wx.showModal({
        title: '提示',
        content: '请填写姓名',
        showCancel: false,
      })
      return;
    }

    register({
      tel: this.data.phone,
      name: this.data.name,
      gender: this.data.genders[this.data.genderIndex],
      role: this.data.roles[this.data.roleIndex],
      birthdate: this.data.birthday,
      linkaddress: this.data.region.join('')
    }, (res) => {
      wx.setStorageSync('isRegistered', true)
      
      wx.showToast({
        title: '注册成功',
        icon: 'success',
        duration: 3000
      });
      app.globalData.isRegistered = true;
      wx.navigateBack({
        delta: 1,
      })
      // wx.switchTab({
      //   url: '../home/home',
      // });
    }, (err) => {
      wx.showModal({
        showCancel: false,
        title: '注册失败',
        content: err || "网络失败，请稍候再试"
      });
      wx.setStorageSync('isRegistered', false)
    });
  }
})