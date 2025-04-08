// pages/activityDetail/activityDetail.ts
import Toast from '@vant/weapp/toast/toast'
import { apiUrl, formatDateTime } from '../../utils/util'
const { request } = require('../../utils/request')
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    navigateBack: true,
    id: '',
    title: '',
    banner: '',
    start_time: '',
    end_time: '',
    isStarted: false,
    isEnd: false,
    date: '',
    address: '',
    location: '',
    fee: '',
    registered_impaired: 0,
    registered_volunteer: 0,
    thumbs_up: 0,
    share: 0,
    isLike: false,
    isRegistered: false,
    isInterested: false,
    isNeedPickup: false,
    notice: '',
    volunteer_capacity: 0,
    volunteer_total: 0,
    volunteer_current: 0,
    vision_impaired_total: 0,
    vision_impaired_current: 0,
    content_location: '',
    content_datetime: '',
    content_service: '',
    content_notice: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.init(options.id)
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
      const content_location = activity.content.split('【活动时间】：')[0].split('【活动地点】：')[1]
      const content_datetime = activity.content.split('【活动时间】：')[1].split('【服务内容】：')[0]
      const content_service = activity.content.split('【活动时间】：')[1].split('【服务内容】：')[1].split('【注意事项】：')[0]
      const content_notice = activity.content.split('【活动时间】：')[1].split('【服务内容】：')[1].split('【注意事项】：')[1]
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
        notice: activity.notice,
        volunteer_label: `${activity.registered_volunteer}/${activity.volunteer_capacity} 志愿者`,
        volunteer_value: (activity.registered_volunteer/activity.volunteer_capacity)*10000,
        vision_impaired_label: `${activity.registered_impaired}/${activity.vision_impaired_capacity} 视障人士`,
        vision_impaired_value: (activity.registered_impaired/activity.vision_impaired_capacity)*10000,
        volunteer_total: activity.volunteer_capacity,
        volunteer_current: activity.registered_volunteer,
        vision_impaired_total: activity.vision_impaired_capacity,
        vision_impaired_current: activity.registered_impaired,
        content_location: content_location,
        content_datetime: content_datetime,
        content_service: content_service,
        content_notice: content_notice
      })
    } catch (error) {
      console.error('请求失败：', error);
    }
  },

  _isRegisteredModal() {
    wx.showModal({
      title: "请先登录或注册，然后报名活动",
      showCancel: true,
      cancelText: "再想想",
      confirmText: "立即注册",
      success: function (res) {
        if (res.confirm) {
          wx.switchTab({
            url: '/pages/my/my'
          })
        }
      }
    })
  },

  _checkActivityStatus() {
    const { start_time_, isActivityStarted } = this.data
    if (start_time_ === '') {
      return false;
    }
    if (isActivityStarted) {

    }
  },

  _updateCurrentValue(isRegistered, isVolunteer) {
    let updated_current = 0
    if (isVolunteer && this.data.volunteer_current) {
      updated_current = this.data.volunteer_current
    } else if (!isVolunteer && this.data.vision_impaired_current) {
      updated_current = this.data.vision_impaired_current
    }
    if (isRegistered) {
      updated_current++
    } else if (updated_current > 0) {
      updated_current--
    }
    return updated_current
  },

  async _toggleRegister(activity_id, isRegistered) {
    if (isRegistered) {
      try {
        Toast.loading({ message: '处理中...', forbidClick: true, duration: 0 })
        const { status, message } = await request('activityParticipant/registerActivity', 'POST', { activity_id })
        if (status === 'success') {
          Toast.success('报名成功')
          if (app.globalData.role === 'volunteer') {
            this.setData({
              isRegistered,
              volunteer_current: this._updateCurrentValue(isRegistered, true)
            })
            // const { id, title, date, address } = this.data
            // wx.navigateTo({
            //   url: `/pages/volunteerSignupSuccess/volunteerSignupSuccess?activity_id=${id}&title=${title}&date=${date}&address=${address}`
            // })
            wx.navigateTo({
              url:  `/pages/activityRegister/activityRegister?id=${activity_id}`
            })
          } else {
            this.setData({
              isRegistered,
              vision_impaired_current: this._updateCurrentValue(isRegistered, false)
            })
          }
        } else if (status === 'failure') {
          Toast.fail(message)
        }
      } catch (error) {
        console.error('请求失败：', error)
      }
    } else {
      try {
        Toast.loading({ message: '处理中...', forbidClick: true, duration: 0 })
        await request('activityParticipant/registerActivity', 'DELETE', { activity_id })
        this.init(activity_id)
        Toast.success('取消报名成功')
      } catch (error) {
        console.error('请求失败：', error)
      }
    }
  },

  onRegisterTap() {
    if (!app.globalData.isRegistered) {
      this._isRegisteredModal()
      return
    }
    let capacity_allow = true
    const current = app.globalData.isVolunteer ? this.data.volunteer_current : this.data.vision_impaired_current
    const total = app.globalData.isVolunteer ? this.data.volunteer_total : this.data.vision_impaired_total
    if (current >= total) {
      capacity_allow = false
    }
    if (capacity_allow || this.data.isRegistered) {
      this._toggleRegister(this.data.id, !this.data.isRegistered)
    } else {
      Toast.fail('报名名额已满')
    }
  },

  async onInterestTap() {
    if (!app.globalData.isRegistered) {
      this._isRegisteredModal()
      return
    }
    try {
      const activity_id = this.data.id
      const isInterested = !this.data.isInterested
      const interest = isInterested ? 1 : 0
      Toast.loading({ message: '处理中...', forbidClick: true, duration: 0 })
      const res = await request(`activity_detail/interest?activity_id=${activity_id}&interest=${interest}`, 'POST', {})
      if (res.status === 'success') {
        this.setData({
          isInterested
        })
        Toast.success(isInterested ? '感兴趣' : '不感兴趣')
      } else {
        Toast.clear()
      }
    } catch (error) {
      console.error('请求失败：', error)
    }
  },

  async onLikeTap() {
    if (!app.globalData.isRegistered) {
      this._isRegisteredModal()
      return
    }
    try {
      const activity_id = this.data.id
      const isLike = !this.data.isLike
      const thumbs_up = isLike ? 1 : 0
      Toast.loading({ message: '处理中...', forbidClick: true, duration: 0 })
      const res = await request(`activity_detail/thumbs_up?activity_id=${activity_id}&thumbs_up=${thumbs_up}`, 'POST', {})
      if (res.status === 'success') {
        this.setData({
          isLike
        })
        Toast.success(isLike ? '点赞' : '取消点赞')
      } else {
        Toast.clear()
      }
    } catch (error) {
      console.error('请求失败：', error)
    }
  },

  onNeedPickupTap(event) {
    console.log('我要接送')
    if (!app.globalData.isRegistered) {
      this._isRegisteredModal()
      return
    }
    const pickupFormForVolunteer = `/pages/pickupFormForVolunteer/pickupFormForVolunteer?activity_id=${this.data.id}`
    const pickupFormForImpaired = `/pages/pickupFormForImpaired/pickupFormForImpaired?activity_id=${this.data.id}`
    wx.navigateTo({
      url: app.globalData.role === 'volunteer' ? pickupFormForVolunteer : pickupFormForImpaired
    })
  },

  onPickupDetailTap(event) {
    console.log('接送详情')
    if (!app.globalData.isRegistered) {
      this._isRegisteredModal()
      return
    }
    const pickupDetailForVolunteer = `/pages/pickupDetailForVolunteer/pickupDetailForVolunteer?activity_id=${this.data.id}`
    const pickupFormForImpaired = `/pages/pickupFormForImpaired/pickupFormForImpaired?activity_id=${this.data.id}`
    wx.navigateTo({
      url: app.globalData.role === 'volunteer' ? pickupDetailForVolunteer : pickupFormForImpaired
    })
  },

  onActivityRegisterTap(event) {
    wx.navigateTo({
      url:  `/pages/activityRegister/activityRegister?id=${event.currentTarget.dataset.activityId}`
    })
  }

})