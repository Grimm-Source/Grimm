const apiUrl = require('../../config.js').apiUrl

Page({

  /**
   * Page initial data
   */
  data: {
    name: '',
    phoneNum: ''
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {

  },

  /**
   * Lifecycle function--Called when page is initially rendered
   */
  onReady: function () {

  },

  /**
   * Lifecycle function--Called when page show
   */
  onShow: function () {

  },

  /**
   * Lifecycle function--Called when page hide
   */
  onHide: function () {

  },

  /**
   * Lifecycle function--Called when page unload
   */
  onUnload: function () {

  },

  /**
   * Page event handler function--Called when user drop down
   */
  onPullDownRefresh: function () {

  },

  /**
   * Called when page reach bottom
   */
  onReachBottom: function () {

  },

  /**
   * Called when user click on the top right corner to share
   */
  onShareAppMessage: function () {

  },

  changeName: function (e) {
    this.setData({
      name : e.detail.value
    })
  },

  changePhoneNum: function (e) {
    this.setData({
      phoneNum: e.detail.value
    })
  },

  submitData: function (e) {
    wx.request({
      url: apiUrl + 'register',
      data: {
        userName: this.data.name,
        phoneNum: this.data.phoneNum
      },
      success: function (res) {
       console.log(res)
      }
    })
  }

})