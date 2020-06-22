const { getActivityDetail, toggleInterest, toggleThumbsUp, toggleRegister} = require('../../utils/requestUtil.js');

const app = getApp();

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
    volunteerTotal: 0,
    volunteerCurr: 0,
    visuallyImpairedTotal: 0,
    visuallyImpairedCurr: 0,
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
    toggleThumbsUp(this.data.id, isLike, () => {
      this.setData({
        isLike
      });
    });
  },
  getActivity: function (){
    getActivityDetail(this.data.id, (res) => {
      this.setData({
        title: res.title,
        isLike: res.interested === 1,
        date: `${res.start_time}至${res.end_time}`,
        address: res.location,
        volunteerTotal: res.volunteer_capacity,
        volunteerCurr: res.volunteers,
        visuallyImpairedTotal: res.vision_impaired_capacity,
        visuallyImpairedCurr: res.vision_impaireds,
        content: `
          ${res.content}

          [注意事项]
          ${res.notice}

          [其他]
          ${res.others}
        `
      })
    });
  },
  onTapRegister: function() {
    const isRegistered = !this.data.isRegistered;
    if( app.globalData.userInfo && app.globalData.userInfo.isRegistered ){
      const isVolunteer = app.globalData.userInfo.role === "志愿者";
      toggleRegister(this.data.id, isRegistered, () => {
        if(isVolunteer){
          this.setData({
            isRegistered,
            volunteerCurr: isRegistered? this.data.volunteerCurr + 1:this.data.volunteerCurr - 1
          });
          return;
        }
        this.setData({
          isRegistered,
          visuallyImpairedCurr: isRegistered? this.data.visuallyImpairedCurr + 1:this.data.visuallyImpairedCurr - 1
        });
      });
      return;
    }
    wx.navigateTo({
      url: '/pages/login/login',
    });
  },
  onTapInterest: function() {
    const isInterested = !this.data.isInterested;
    toggleInterest(this.data.id, isInterested, () => {
      this.setData({
        isInterested
      });
    });
  }
})
