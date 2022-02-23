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
    idNo: '',
    impairedNo: '',
    email: ''
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

  bindIdNoChange: function (e) {
    this.setData({
      idNo : e.detail.value
    })
  },

  bindImpairedNoChange: function (e) {
    this.setData({
      impairedNo : e.detail.value
    })
  },

  bindEmailChange: function (e) {
    this.setData({
      email : e.detail.value
    })
  },

  onImpairedSelected: function() {
    this.setData({
      showModal: false,
      role: "impaired",
      roleIndex: 0
    })
  },

  onVolunteerSelected: function() {
    this.setData({
      showModal: false,
      role: "volunteer",
      roleIndex: 1
    })
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
        content: '请填写真实姓名',
        showCancel: false,
      })
      return;
    }
    if (this.data.role == 'impaired' && !this.data.impairedNo) {
      wx.showModal({
        title: '提示',
        content: '请填写残疾证号',
        showCancel: false,
      })
      return;
    }
    var idReg = /^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10|11|12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx]$/;
    var passportReg = /^([a-zA-z]|[0-9]){5,17}$/;
    if (!idReg.test(this.data.idNo) && !passportReg.test(this.data.idNo)) {
      wx.showModal({
        title: '提示',
        content: '请填写正确的身份证号/护照号',
        showCancel: false,
      })
      return;
    }

    if (this.data.impairedNo && !/^\d{17}[\d|x]\d{2}$/i.test(this.data.impairedNo)) {
      wx.showModal({
        title: '提示',
        content: '请填写正确的残疾证号',
        showCancel: false,
      })
      return;
    }
    var emailReg = /^[A-Za-z0-9]+([-_.][A-Za-z0-9]+)*@([A-Za-z0-9]+[-.])+[A-Za-zd]{2,5}$/;
    if (!this.data.email) {
      wx.showModal({
        title: '提示',
        content: '请填写邮箱',
        showCancel: false,
      })
      return;
    }
    if (this.data.email && !emailReg.test(this.data.email)) {
      wx.showModal({
        title: '提示',
        content: '请填写正确的邮箱地址',
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
      idcard: this.data.idNo,
      disabledID: this.data.impairedNo,
      email: this.data.email,
      avatarUrl: app.globalData.userInfo.avatarUrl
    }, (res) => {
      app.globalData.isRegistered = true;
      app.globalData.isVolunteer = this.data.role == 'volunteer' ? true : false;
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
