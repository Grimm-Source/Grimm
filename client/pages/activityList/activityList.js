const {getActivityList, getRegisteredActivityList} = require('../../utils/requestUtil.js');

const type = {
    ALL: "ALL",
    REGISTERED: "REGISTERED"
};

Page({
  data: {
    activityList: [],
    activityListUi: [],
    type: type.ALL
  },
  //事件处理函数
  onLoad: function (options) {
    this.setData({
        type: type[options.type]? type[options.type]: type.ALL
    })
  }, 
  onPullDownRefresh: function () {
    this.data.type === type.ALL? this.getActivities(): this.getRegisteredActivities();
  },
  onShow: function () {
    this.data.type === type.ALL? this.getActivities(): this.getRegisteredActivities();
  },
  getActivities: function (){
    getActivityList((res)=>{
        var uiList = this.getActivityListUi(res)
        this.setData({
          activityList: res,
          activityListUi: uiList
        })
    }); 
  },
  getRegisteredActivities: function(){
    getRegisteredActivityList(null, (res)=>{
        var uiList = this.getActivityListUi(res)
        this.setData({
          activityList: res,
          activityListUi: uiList
        })
    })
  },
  
  getActivityListUi: function(obj){
    var uiList = JSON.parse(JSON.stringify(obj));
    uiList.forEach((item)=>{
      item.startTimeStamp = new Date(item.start_time).getTime();
    });
    return uiList;
  },
  onTapActivity: function(event){
    let item = event.currentTarget.dataset && event.currentTarget.dataset.item,
    activityId = this.data.type === type.ALL? item.id : item.activity_id;
    console.log(111)
    wx.navigateTo({
        url: '/pages/activityDetail/activityDetail?activity_id='+ activityId,
    })
  }
})
