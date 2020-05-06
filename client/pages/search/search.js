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
    const arr = [
      {"adminId": 0, "content": "test", "duration": {"day": 1, "hour": 0, "min": 13, "sec": 0}, "end_time": "2020-04-11T12:00:00", "id": 9, "location": "Shanghai", "notice": "test", "others": "", "start_time": "2020-04-10T11:47:00", "tag": "其它,保健", "title": "test1"}, 
      {"adminId": 0, "content": "测试数据", "duration": {"day": 4, "hour": 0, "min": 2, "sec": 0}, "end_time": "2020-04-14T15:09:00", "id": 8, "location": "上海人民广场", "notice": "测试数据", "others": "交通安全", "start_time": "2020-04-10T15:07:00", "tag": "分享,文娱,学习", "title": "集善助盲摄影作品展"}, 
      {"adminId": 0, "content": "待完善", "duration": {"day": 4, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-04-02T14:12:33", "id": 4, "location": "北京王府井新燕莎金街购物广场", "notice": "待完善", "others": "", "start_time": "2020-03-29T14:12:33", "tag": "保健,其它", "title": "全新大型公益互动体验“非视觉太极”活动月"}, 
      {"adminId": 0, "content": "阴天，宅家，吃饭睡觉打豆豆", "duration": {"day": 1, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-03-30T09:44:24", "id": 3, "location": "Beijing", "notice": "阴天，宅家，吃饭睡觉打豆豆", "others": "", "start_time": "2020-03-29T09:44:24", "tag": "分享,文娱", "title": "今天是阴天"}, 
      {"adminId": 0, "content": "春暖花开，一起出门放风筝。", "duration": {"day": 1, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-03-27T16:29:40", "id": 2, "location": "zhejiang", "notice": "春暖花开，一起出门放风筝。", "others": "", "start_time": "2020-03-26T16:29:40", "tag": "运动,文娱,保健", "title": "今天天气好"}
    ]
    const newArr = [];
    const searchWord = this.data.selelctedVal + searchVal;
    arr.forEach(item => {
      if(item.title.includes(searchWord)){
        let startTime = item.start_time.replace('T', ' ');
        let endTime = item.end_time.replace('T', ' ');
        let time = `${startTime}-${endTime}`;
        item.time = time;
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