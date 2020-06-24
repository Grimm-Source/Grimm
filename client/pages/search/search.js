// pages/search/search.js
const { searchActivity } = require('../../utils/requestUtil');
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
    const newArr = [];
    const searchWord = this.data.selelctedVal + searchVal;
    
    searchActivity(searchWord, (res) => {
      res.forEach(item => {
        if(item.title.includes(searchWord)){
          newArr.push(item)
        }
      })
      const arr_copy = newArr.slice();
      if(arr_copy && arr_copy.length > 0){
        arr_copy.forEach(item => {
          const newTitle = this._highlightWord(searchWord, item)
          const formatTime = this._activitySchedule(item)
          item.title = newTitle;
          item.schedule = formatTime
        });
      }
      this.setData({
        searchValue: searchVal,
        searchedActivities: arr_copy
      })
    })
  },

  _highlightWord: function(searchWord, activity){
    let newStr = activity.title;
    const titleArr = []
    if(searchWord.length > 0 && activity.title.indexOf(searchWord) > -1){
      newStr = activity.title.split(searchWord).join(`<span>${searchWord}<span>`);
      const wordArr = newStr.split('<span>');
      wordArr.forEach(item => {
        if(searchWord === item){
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
    }else{
      titleArr.push({
        word: newStr,
        className: 'black'
      })
    }

    return titleArr;
  },

  _activitySchedule: function(activity){
    let startTime = activity.start_time.replace('T', ' ').replace(/-/g, ".");
    let endTime = activity.end_time.replace('T', ' ').replace(/-/g, ".");
    let timeStr = "";
    if (activity.duration.day != 0) {
      timeStr = startTime.substr(0, 10) + " - " + endTime.substr(0, 10)
    } else {
      timeStr = startTime.substr(0, 16) + "-" + endTime.substr(11, 16)
    }
    return timeStr;
  }
})