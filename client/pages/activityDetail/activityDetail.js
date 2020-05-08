const { getActivityDetail, toggleInterest, toggleThumbsUp, toggleRegister} = require('../../utils/requestUtil.js');
const app = getApp()

Page({
  data: {
    banner: '/images/banner.jpg',
    title: '',
    isLike: false,
    date: '',
    address: '',
    content: '',
    isRegistered: false,
    isInterested: false,
    volunteerTotal: 50,
    volunteerCurr: 0,
    visuallyImpairedTotal: 50,
    visuallyImpairedCurr: 0,
    likeNum: 0
  },
  //事件处理函数
  onLoad: function (option) {
    this.setData({
      id: option.id
    });
  }, 
  onPullDownRefresh: function () {
    this.getActivity();
  },
  onShow: function () {
   this.getActivity();
  },
  onTapLike: function() {
    const isLike = !this.data.isLike;
    // toggleLike(this.data.id, isLike, () => {
    this.setData({
      isLike
    });
    if(this.data.isLike){
      this.setData({likeNum: this.data.likeNum + 1})
    }else if(this.data.likeNum === 0){
      this.setData({likeNum: 0})
    }else{
      this.setData({likeNum: this.data.likeNum - 1})
    }

    const that = this;

    let result = app.globalData.activityList.findIndex(function(object) {
      return object.id === Number(that.data.id);
    });
    app.globalData.activityList[result].likeNum = this.data.likeNum;
    app.globalData.activityList[result].isLike = this.data.isLike;
    // });
  },
  getActivity: function (){
    // getActivityDetail(this.data.id, (res) => {
    //   this.setData({
    //     title: res.title,
    //     isLike: res.interested === 1,
    //     likeNum: Number(this.data.id),
    //     date: `${res.start_time}至${res.end_time}`,
    //     address: res.location,
    //     volunteerTotal: res.volunteer_capacity,
    //     volunteerCurr: res.volunteers,
    //     visuallyImpairedTotal: res.vision_impaired_capacity,
    //     visuallyImpairedCurr: res.vision_impaireds,
    //     content: `
    //       ${res.content}

    //       [注意事项]
    //       ${res.notice}

    //       [其他]
    //       ${res.others}
    //     `
    //   })
    // });
    app.globalData.activityList.forEach(item => {
      if(item.id === Number(this.data.id)){
        let startTime = item.start_time.replace('T', ' ');
        let startTimeLastIndex = startTime.lastIndexOf(':')
        let endTime = item.end_time.replace('T', ' ');
        let endTimeLastIndex = endTime.lastIndexOf(':')
        this.setData({
          title: item.title,
          isLike: item.isLike,
          likeNum: item.likeNum,
          isInterested: item.isInterested,
          isRegistered: item.registered,
          date: `${startTime.substring(0, startTimeLastIndex)}至${endTime.substring(0, endTimeLastIndex)}`,
          address: item.location,
          volunteerTotal: item.volunteer_capacity,
          volunteerCurr: item.volunteers,
          visuallyImpairedTotal: item.vision_impaired_capacity,
          visuallyImpairedCurr: item.vision_impaireds,
          content: `
            ${item.content}
  
            [注意事项]
            ${item.notice}
  
            [其他]
            ${item.others}
          `
        })
      }
    });
  },
  onTapRegister: function() {
    // const isRegistered = !this.data.isRegistered;
    // toggleRegister(this.data.id, isRegistered, () => {
    //   this.setData({
    //     isRegistered
    //   });
    // });
    const isRegistered = !this.data.isRegistered;
    if(app.globalData.isRegistered){
      let toastTitle = isRegistered ? '报名成功' : '取消报名'
      wx.showToast({
        title: toastTitle,
        icon: 'none',
        duration: 2000
      });
      const that = this;
      let result = app.globalData.activityList.findIndex(function(object) {
        return object.id === Number(that.data.id);
      });
      app.globalData.activityList[result].registered = isRegistered;
      this.setData({
        isRegistered
      })
    }else{
      wx.navigateTo({
        url: '/pages/login/login',
      })
    }
  },
  onTapInterest: function() {
    const isInterested = !this.data.isInterested;
    const that = this;
    let result = app.globalData.activityList.findIndex(function(object) {
      return object.id === Number(that.data.id);
    });
    app.globalData.activityList[result].isInterested = isInterested;
    // toggleRegister(this.data.id, isInterested, () => {
        this.setData({
          isInterested
        });
    // });
  }
})
