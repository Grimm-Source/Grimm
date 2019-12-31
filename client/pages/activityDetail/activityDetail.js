const {getProfile, getRegisteredActivityList, removeRegisteredActivityList, getActivity} = require('../../utils/requestUtil.js');

Page({
  data: {
    activity: {},
    activityUi: {},
    activityId: null,
    isRegistered: false
  },
  //事件处理函数
  onLoad: function (option) {
    if(!option.activityId){
      return;
    }
    this.setData({
        activityId: option.activityId
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
      if(res.length < 1){
        getActivity(this.data.activityId, (res)=>{
          let activityUi = this.getActivityUi(res);
          this.setData({
            activity: res,
            activityUi,
            isRegistered: false
          })
        },()=>{

        })
        return;
      }
        let activityUi = this.getActivityUi(res[0]);
        this.setData({
          activity: res[0],
          activityUi,
          isRegistered: true
        });
        this.getContactInfo();
    }); 
  },
  
  getActivityUi: function(obj){
    var activity = JSON.parse(JSON.stringify(obj));
    activity.startTimeStamp = new Date(activity.start_time).getTime();
    activity.endTimeStamp = new Date(activity.end_time).getTime();
    return activity;
  },
  onTapApply: function(event){
    let activityId = this.data.activityId;
    wx.navigateTo({
        url: '/pages/application/application?activityId='+ activityId
    });
  },
  getContactInfo: function (){
    getProfile((res)=>{
        this.setData({
          role: res.role
        })
    }); 
  },

  onTapCancel: function(event){
    removeRegisteredActivityList([this.data.activityId], ()=>{
      this.getActivity();
    });
  }

})
