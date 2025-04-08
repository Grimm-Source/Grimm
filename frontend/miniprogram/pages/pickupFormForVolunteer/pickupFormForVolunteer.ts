// pages/pickupFormForVolunteer/pickupFormForVolunteer.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    id: '',
    title: '',
    banner: '',
    start_time: '',
    end_time: '',
    current: [],
    options: [
      {
        value: '0', name: '接视障人士参加活动', items: [
          {value: '0_1', name: '私家车'},
          {value: '0_2', name: '步行地铁'}
        ]
      },
      {
        value: '1', name: '送视障人士回家', items: [
          {value: '1_0', name: '私家车'},
          {value: '1_1', name: '步行地铁'}
        ]
      },
      {
        value: '2', name: '接送视障人士参加活动', items: [
          {value: '2_0', name: '私家车'},
          {value: '2_1', name: '步行地铁'}
        ]
      },
    ],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.init(options.activity_id)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  async init(id) {
    try {
      Toast.loading({ message: '处理中...', forbidClick: true, duration: 0 })
      const activity = await request(`activity_detail?activity_id=${id}`, 'GET', {})
      Toast.clear()
      this.setData({
        id: activity.id,
        title: activity.title,
        banner: `${apiUrl}activity/themePic?activity_them_pic_name=${activity.activity_them_pic_name}`,
        start_time: formatDateTime(activity.start_time),
        end_time: formatDateTime(activity.end_time),
        start_time_: activity.start_time.replace('T', ' '),
        end_time_: activity.end_time.replace('T', ' '),
        isActivityStarted: Date.now() > Date.parse(activity.start_time),
        isActivityEnd: Date.now() > Date.parse(activity.end_time),
        date: `${activity.start_time.replace('T', ' ').substr(0, 16)} 至 ${activity.end_time.replace('T', ' ').substr(0, 16)}`,
        address: activity.location,
        location: activity.location,
        fee: activity.activity_fee > 0 ? `¥${activity.activity_fee}元` : '免费',
        registered_impaired: activity.registered_impaired,
        registered_volunteer: activity.registered_volunteer,
        thumbs_up: activity.thumbs_up,
        share: activity.share,
        isLike: activity.thumbs_up === 1,
        isRegistered: activity.registered === 1,
        isInterested: activity.interested === 1,
        isNeedPickup: activity.needPickup === 1,
      })
    } catch (error) {
      console.error('请求失败：', error);
    }
  },

  onCheckboxChange(event) {
    this.setData({
      current: event.detail
    })
  },

  onSubmitTap() {
    try {
      const { name, idcard, region } = this.data
      const params = { name, idcard, region }
      if (this._verify(name, idcard, region)) {
        Toast.loading({ message: '加载中...', forbidClick: true, duration: 0 })
      }

    } catch (error) {
      console.error('请求失败：', error)
    }
  },

  _verify(name, idcard, region) {
    if (name === '') {
      wx.showModal({ title: '错误提示', content: '请填写真实姓名', showCancel: false })
      return false
    }
    if (region === '') {
      wx.showModal({ title: '错误提示', content: '请选择所在城区', showCancel: false })
      return false
    }
    var idReg = /^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10|11|12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx]$/
    if (idcard === '') {
      wx.showModal({ title: '错误提示', content: '请填写身份证号', showCancel: false })
      return false
    }
    // } else if (idcard && !idReg.test(idcard)) {
    //   wx.showModal({ title: '错误提示', content: '请填写正确的身份证号', showCancel: false })
    //   return false
    // }
    return true
  },
})