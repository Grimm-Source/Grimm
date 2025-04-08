// pages/activityList/activityList.ts
const { request } = require('../../utils/request')
import Toast from '@vant/weapp/toast/toast'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    background: [
      'https://www.rp-i.net/images/activity_theme_pictures/20200829-茶话会-第89期活动-视障伙伴体验踢足球.JPG',
      'https://www.rp-i.net/images/activity_theme_pictures/20200830-世纪公园-第88期活动-进公园活动前，大家要先过条大马路.JPG',
      'https://www.rp-i.net/images/activity_theme_pictures/20200823-黛墨软装展厅-第86期活动-开心大合照.JPG'
    ],
    indicatorDots: false,
    autoplay: true,
    circular: true,
    interval: 10000,
    duration: 500,
    categoryList: [
      { text: '不限活动类型', value: 0 },
      { text: '运动', value: 1 },
      { text: '学习', value: 2 },
      { text: '分享', value: 3 },
      { text: '文娱', value: 4 },
      { text: '保健', value: 5 },
      { text: '其它', value: 6 },
    ],
    timeList: [
      { text: '不限活动时间', value: 'all' },
      { text: '最新', value: 'latest' },
      { text: '周末', value: 'weekends' },
      { text: '最近一周', value: 'recents' },
    ],
    category: 0,
    time: 'all',
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
    this._getFilteredActivities()
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
      Toast.loading({ message: '加载中...', forbidClick: true, duration: 0 })
      const data = await request('activities', 'GET', {});
      this.setData({
        activityList: data
      });
      Toast.clear()
    } catch (error) {
      console.error('请求失败：', error);
    }
  },

  async _getFilteredActivities() {
    try {
      Toast.loading({ message: '加载中...', forbidClick: true, duration: 0 })
      this.setData({
        activityList: []
      });
      let filteredParams = this.data.category !== -1 ? `tags=${this.data.category}&` : '';
      filteredParams += this.data.time !== 'all' ? `time=${this.data.time}` : '';
      const data = await request(`activities?${filteredParams}`, 'GET', {});
      this.setData({
        activityList: data
      });
      Toast.clear()
      wx.stopPullDownRefresh()
      wx.hideNavigationBarLoading()
    } catch (error) {
      console.error('请求失败：', error);
    }
  },

  onChangeCategory(event) {
    this.setData({
      category: event.detail
    })
    this._getFilteredActivities()
  },

  onChangeTime(event) {
    this.setData({
      time: event.detail
    })
    this._getFilteredActivities()
  },
})