// pages/search/search.js
Page({

  /**
   * Page initial data
   */
  data: {
    searchValue: null,
    selelctedVal: '',
    placeHolder: '关键词搜索',
    wordList: [
      {
        value: '预设词1'
      },{
        value: '预设词2'
      },{
        value: '超长超长超长超长预设词'
      },{
        value: '预设词3'
      },{
        value: '预设词4'
      },
      {
        value: '预设词5'
      }
    ]
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

  selectSearchWord: function(e) {
    const searchWord = e.currentTarget.dataset.search;
    
    this.setData({
      selelctedVal: searchWord,
      placeHolder: ''
    })
  },

  cancelSelect: function() {
    this.setData({
      selelctedVal: '',
      placeHolder: '关键词搜索'
    })
  }
})