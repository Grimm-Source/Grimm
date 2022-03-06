const {
  pickUpImpaired,
  getCurrentUserDetail
} = require('../../utils/requestUtil.js');

const app = getApp();

Page({
  data: {
    name: '', //接送人员真实姓名
    idNo: '', //身份证号
    impairedNo: '', //残疾证号
    pickupAddr: '', //接送的起始位置
    emergencyContact: '', //紧急联系人电话
    activity_id: '', //活动id
  },

  onLoad: function (options) {
    this.setData({
      activity_id: options.activity_id,
      title: options.title == 'undefined' ? '': options.title,
      date: options.date == 'undefined' ? '': options.date,
      address: options.address == 'undefined' ? '': options.address,
    })
    if (options.willPickup === "1") {
      getCurrentUserDetail((res) => {
        this.setData({
          name: res.name, //接送人员真实姓名, 默认填充当前授权用户名字
          idNo: res.id_type == '身份证' ? res.idcard: '', //默认填充当前授权用户身份证号
          impairedNo: res.disabled_id, //默认填充当前授权用户残疾证号
        })
      });
    }else {
      getCurrentUserDetail((res) => {
        this.setData({
          name: res.name, //接送人员真实姓名, 默认填充当前授权用户名字
          idNo: res.id_type == '身份证' ? res.idcard: '', //默认填充当前授权用户身份证号
          impairedNo: res.disabled_id, //默认填充当前授权用户残疾证号
        })
      });
      this.setData({
        //name: options.name == 'undefined' ? '': options.name, //接送人员真实姓名
        //idNo: options.idNo == 'undefined' ? '': options.idNo, //身份证号
        //impairedNo: options.impairedNo == 'undefined' ? '': options.impairedNo, //残疾证号
        pickupAddr: options.pickupAddr == 'undefined' ? '': options.pickupAddr,//接送的起始位置
        emergencyContact: options.emergencyContact == 'undefined' ? '': options.emergencyContact, //紧急联系人电话
      })
    }
  },

  changeName: function (e) {
    this.setData({
      name: e.detail.value
    })
  },
  changeIdNo: function (e) {
    this.setData({
      idNo: e.detail.value
    })
  },
  changeImpairedNo: function (e) {
    this.setData({
      impairedNo: e.detail.value
    })
  },
  changePickupAddr: function (e) {
    this.setData({
      pickupAddr: e.detail.value
    })
  },
  changeEmergencyContact: function (e) {
    this.setData({
      emergencyContact: e.detail.value
    })
  },

  onSubmit: function () {

    if (!this.data.name) {
      wx.showModal({
        title: '提示',
        content: '请填写真实姓名',
        showCancel: false,
      })
      return;
    }

    var idReg = /^(([1][1-5])|([2][1-3])|([3][1-7])|([4][1-6])|([5][0-4])|([6][1-5])|([7][1])|([8][1-2]))\d{4}(([1][9]\d{2})|([2]\d{3}))(([0][1-9])|([1][0-2]))(([0][1-9])|([1-2][0-9])|([3][0-1]))\d{3}[0-9xX]$/;
    var passportReg = /^([a-zA-z]|[0-9]){5,17}$/;
    if (!idReg.test(this.data.idNo) && !passportReg.test(this.data.idNo)) {
      wx.showModal({
        title: '提示',
        content: '请填写正确的身份证号/护照号',
        showCancel: false,
      })
      return;
    }

    if (!this.data.impairedNo) {
      wx.showModal({
        title: '提示',
        content: '请填写残疾证号',
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

    if (!this.data.pickupAddr) {
      wx.showModal({
        title: '提示',
        content: '请填写起始位置',
        showCancel: false,
      })
      return;
    }

    if (!this.data.emergencyContact) {
      wx.showModal({
        title: '提示',
        content: '请填写紧急联系人电话',
        showCancel: false,
      })
      return;
    }

    pickUpImpaired({
      name: this.data.name,
      idNo: this.data.idNo,
      impairedNo: this.data.impairedNo,
      pickupAddr: this.data.pickupAddr,
      emergencyContact: this.data.emergencyContact,
      activity_id: this.data.activity_id,
    }, (res) => {
      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000,
        mask: true,
        success: function () {
          setTimeout(function () {
            wx.navigateBack({
              delta: 1
            });
          }, 2000)
        },
      });
    }, (err) => {
      wx.showModal({
        showCancel: false,
        title: '提交失败',
        content: err || "网络失败，请稍候再试"
      });
    });
  }
})
