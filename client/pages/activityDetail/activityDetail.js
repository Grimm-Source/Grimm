const {getRegisteredActivityList} = require('../../utils/requestUtil.js');

Page({
  data: {
    activity: {},
    activityUi: {},
    activityId: null
  },
  //事件处理函数
  onLoad: function (option) {
    if(!option.activityId){
      return;
    }
    this.setData({
        activityId: option.activityId,
        activity: JSON.parse(option.item),
        activityUi: this.getActivityUi(JSON.parse(option.item))
    });
  }, 
  onPullDownRefresh: function () {
    this.getActivity();
  },
  onShow: function () {
   this.getActivity();
  },
  getActivity: function (){
    getRegisteredActivityList([this.data.activityId], (res)=>{
        var activityUi = this.getActivityUi(res)
        this.setData({
          activity: res,
          activityUi
        })
    }); 
  },
  
  getActivityUi: function(obj){
    var activity = JSON.parse(JSON.stringify(obj));
    activity.startTimeStamp = new Date(activity.start_time).getTime();
    activity.endTimeStamp = new Date(activity.end_time).getTime();
    return activity;
  },
  onTapApply: function(event){
    let item = event.currentTarget.dataset && event.currentTarget.dataset.item,
    activityId = item.id || null;
    wx.navigateTo({
        url: '/pages/application/application?activityId='+ activityId
    })
  }

})
