const {
  pickUpVolunteer,
  getCurrentUserDetail
} = require('../../utils/requestUtil.js');

Page({
  data: {
    activity_id: '',
    name: '',
    idNo: '',
    pickupAddr: '',
    provideService: '',
    items: [
      {value: '0', name: '接视障人士参加活动',items:[
        {value: '0_0', name: '私家车'},
        {value: '0_1', name: '步行地铁'}
      ]},
      {value: '1', name: '送视障人士回家',items:[
        {value: '1_0', name: '私家车'},
        {value: '1_1', name: '步行地铁'}
      ]},
      {value: '2', name: '接送视障人士参加活动',items:[
        {value: '2_0', name: '私家车'},
        {value: '2_1', name: '步行地铁'}
      ]},
    ],
    title: '',
    date: '',
    address: '',
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
        })
      });
    }
  },

  changeName: function(e) { this.setData({ name: e.detail.value }) },
  changeIdNo: function(e) { this.setData({ idNo: e.detail.value }) },
  changePickupAddr: function(e) { this.setData({ pickupAddr: e.detail.value }) },

  checkboxChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    this.setData({ provideService: e.detail.value })
    const items = this.data.items
    const values = e.detail.value
    for (let i = 0, lenI = items.length; i < lenI; ++i) {
      items[i].checked = false
      for (let x = 0, lenX = items[i].items.length; x < lenX; ++x) {
        items[i].items[x].checked = false
        for (let j = 0, lenJ = values.length; j < lenJ; ++j) {
          if(items[i].items[x].value === values[j]){
            items[i].items[x].checked = true
            break
          }
        } 
       } 
       for (let j = 0, lenJ = values.length; j < lenJ; ++j) {
        if (items[i].value === values[j]) {
          items[i].checked = true
          break
        }
      } 
    }

    this.setData({
      items
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

    if (!this.data.pickupAddr) {
      wx.showModal({
        title: '提示',
        content: '请填写所在区域',
        showCancel: false,
      })
      return;
    }

    if (!this.data.provideService || this.data.provideService.length == 0) {
      wx.showModal({
        title: '提示',
        content: '请填写您可以提供的志愿者服务',
        showCancel: false,
      })
      return;
    }

    pickUpVolunteer({
      name: this.data.name,
      idNo: this.data.idNo,
      pickupAddr: this.data.pickupAddr,
      provideService: this.data.provideService.join(','),
      activity_id: this.data.activity_id,
    }, (res) => {
      let that = this
      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000,
        mask: true,
        success: function () {
          let url = '../pickupVolunteerDetail/pickupVolunteerDetail?activity_id=' + that.data.activity_id + '&'
          url = url + 'title=' + that.data.title + '&'
          url = url + 'date=' + that.data.date + '&'
          url = url + 'address=' + that.data.address + '&'
          setTimeout(function () {
            wx.navigateTo({
              url: url,
            })
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
