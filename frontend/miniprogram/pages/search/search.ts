// pages/search/search.ts
const { request } = require('../../utils/request')
import Toast from '@vant/weapp/toast/toast'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    value: '',
    focus: true,
    activityList: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {

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
    if (this.data.value !== '') {
      this.fetchData()
    } else {
      wx.stopPullDownRefresh()
      wx.hideNavigationBarLoading()
    }
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

  onChange(event) {
    if (event.detail === '') {
      this.setData({
        value: event.detail,
        activityList: []
      })
    }
  },

  onSearch(event) {
    if (event.detail !== '') {
      this.setData({
        value: event.detail
      })
      this.fetchData()
    }
  },
  
  async fetchData() {
    try {
      Toast.loading({
        message: '加载中...',
        forbidClick: true,
        duration: 0,
      })
      this.setData({
        activityList: []
      })
      const data = await request(`activities?keyword=${this.data.value}`, 'GET', {})
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
})