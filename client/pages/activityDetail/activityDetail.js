const {getProfile, getRegisteredActivityList, removeRegisteredActivityList, getActivity} = require('../../utils/requestUtil.js');

Page({
  data: {
    banner: '/images/banner.jpg',
    title: '#世纪公园新年暴走活动,爱心助盲招募志愿者#',
    isLike: false,
    date: '2020.2.29 13:00-15:00',
    address: '上海世纪公园',
    content: `
      您需要做什么?
      A. 抽出一个下午的时间,在地铁站等候视障人士,带他们一起走进电影院,路上可以和他们聊天,谈天说地.
      B. 提前支付您和视障人士的电影票款(以便提前预定座位,保证观影活动的顺利进行)
      C. 观影结束,护送视障人士到最近的地铁站,交接给地铁工作人员.

      Q&A:
      1....
      2....
      3....
    `
  },
  //事件处理函数
  onLoad: function (option) {
    // if(!option.activityId){
    //   return;
    // }
    // this.setData({
    //     activityId: option.activityId
    // });
  }, 
  onPullDownRefresh: function () {
    // this.getActivity();
  },
  onShow: function () {
  //  this.getActivity();
  },
  onTapLike: function() {
    this.setData({
      isLike: !this.data.isLike
    })
  },
  onTapShare: function () {
    console.log('share')
  }
  // getActivity: function (){
  //   getRegisteredActivityList([this.data.activityId], (res)=>{
  //     if(res.length < 1){
  //       getActivity(this.data.activityId, (res)=>{
  //         let activityUi = this.getActivityUi(res);
  //         this.setData({
  //           activity: res,
  //           activityUi,
  //           isRegistered: false
  //         })
  //       },()=>{

  //       })
  //       return;
  //     }
  //       let activityUi = this.getActivityUi(res[0]);
  //       this.setData({
  //         activity: res[0],
  //         activityUi,
  //         isRegistered: true
  //       });
  //       this.getContactInfo();
  //   }); 
  // },
  
  // getActivityUi: function(obj){
  //   var activity = JSON.parse(JSON.stringify(obj));
  //   activity.startTimeStamp = new Date(activity.start_time).getTime();
  //   activity.endTimeStamp = new Date(activity.end_time).getTime();
  //   return activity;
  // },
  // onTapApply: function(event){
  //   let activityId = this.data.activityId;
  //   wx.navigateTo({
  //       url: '/pages/application/application?activityId='+ activityId
  //   });
  // },
  // getContactInfo: function (){
  //   getProfile((res)=>{
  //       this.setData({
  //         role: res.role
  //       })
  //   }); 
  // },

  // onTapCancel: function(event){
  //   removeRegisteredActivityList([this.data.activityId], ()=>{
  //     this.getActivity();
  //   });
  // }

})
