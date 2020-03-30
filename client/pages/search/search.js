// pages/search/search.js
Page({

  /**
   * Page initial data
   */
  data: {
    searchValue: null,
    selelctedVal: '',
    placeHolder: '关键词搜索',
    focus: true,
    wordList: [
      {
        value: '预设词1'
      },{
        value: '预设词2'
      },{
        value: '超长超长超长预设词'
      },{
        value: '预设词3'
      },{
        value: '预设词4'
      },
      {
        value: '预设词5'
      }
    ],
    searchedActivities: null
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
      placeHolder: '',
      focus: true
    })
  },

  cancelSelect: function() {
    this.setData({
      selelctedVal: '',
      placeHolder: '关键词搜索'
    })
  },

  searchActivities: function(e){
    const keyCode = e.detail.keyCode;
    if(keyCode === 8){
      this.cancelSelect();
    }
  },

  endsearchActivities: function(e){
    const searchVal = e.detail.value;
    const arr = [{ 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年走走走陪走活动走走走走活动活动', state: 'joined', statestring: '报名成功' },
    { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年陪走活动', state: 'interested', statestring: '感兴趣' },
    { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年活动', state: 'joined', statestring: '报名成功' },
    { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年活动', state: 'interested', statestring: '感兴趣' }]
    const newArr = [];
    const searchWord = this.data.selelctedVal + searchVal;
    arr.forEach(item => {
      if(item.title.includes(searchWord)){
        newArr.push(item)
      }
    })
    // searchActivity(this.properties.searchedVal, (res) => {
        
    // })
    const arr_copy = newArr.slice();
    if(arr_copy && arr_copy.length > 0){
      arr_copy.forEach(item => {
        const wordArr = item.title.split('');
        const titleArr = []
        wordArr.forEach(item => {
          if(searchWord.includes(item)){
            titleArr.push({
              word: item,
              className: 'green'
            })
          }else{
            titleArr.push({
              word: item,
              className: 'black'
            })
          }
        })
        item.title = titleArr;
      });
    }
    
    this.setData({
      searchValue: searchVal,
      searchedActivities: arr_copy
    })
  }
})