const { register} = require('../../utils/requestUtil.js');
const app = getApp();
Page({
  data: {
    phone: '',
    name: '',
    genders: ['男', '女'],
    genderIndex: 0,
    birthday: '',
    region: [],
    role: '',
    roleShow: ['视障者','志愿者'],
    roleIndex: 0, //0:impaired 1:volunteer
    showModal: true,
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

  onImpairedSelected: function() {
    this.setData({
      showModal: false,
      role: "impaired",
      roleIndex: 0
    })
    app.globalData.roleIndex = roleIndex;
  },

  onVolunteerSelected: function() {
    this.setData({
      showModal: false,
      role: "volunteer",
      roleIndex: 1
    })
    app.globalData.roleIndex = roleIndex;
  },

  onRoleChanged: function(e) {
    if (e.detail.value == 0) {
      this.onImpairedSelected();
    }
    else {
      this.onVolunteerSelected();
    }
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
      phone: this.data.phone,
      name: this.data.name,
      gender: this.data.genders[this.data.genderIndex],
      birthdate: this.data.birthday,
      linkaddress: this.data.region.join(''),
      role: this.data.role,
    }, (res) => {
      app.globalData.isRegistered = true;
      wx.showToast({
        title: '注册成功',
        icon: 'success',
        duration: 3000
      });
      wx.switchTab({
        url: '../home/home',
      });
    }, (err) => {
      wx.showModal({
        showCancel: false,
        title: '注册失败',
        content: err || "网络失败，请稍候再试"
      });
      app.globalData.isRegistered = false;
    });
  }
})