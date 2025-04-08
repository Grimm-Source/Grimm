// pages/myActivityList/myActivityList.ts
const { request } = require('../../utils/request')
import Toast from '@vant/weapp/toast/toast'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    active: 0,
    filter: 'all',
    activityList: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.init()
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
    wx.showNavigationBarLoading()
    this.init()
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

  async init() {
    try {
      Toast.loading({
        message: '加载中...',
        forbidClick: true,
        duration: 0,
      })
      // const data = await request('activities', 'GET', {})
      const data = await request(`myActivities?filter=${this.data.filter}`, 'GET', {})
      this.setData({
        activityList: data
      })
      Toast.clear()
      wx.stopPullDownRefresh()
      wx.hideNavigationBarLoading()
    } catch (error) {
      console.error('请求失败：', error)
    }
  },

  onChange(event) {
    let filter = ''
    if (event.detail.name === 0) {
      filter = 'all'
    } else if (event.detail.name === 1) {
      filter = 'registered'
    } else if (event.detail.name === 2) {
      filter = 'favorite'
    } else if (event.detail.name === 3) {
      filter = 'end'
    }
    this.setData({
      filter
    })
    this.init()
  }
})