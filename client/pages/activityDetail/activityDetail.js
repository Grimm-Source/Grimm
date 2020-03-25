const { getActivityDetail, toggleInterest, toggleThumbsUp, toggleRegister} = require('../../utils/requestUtil.js');

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
    toggleLike(this.data.id, isLike, () => {
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
    // const isRegistered = !this.data.isRegistered;
    // toggleRegister(this.data.id, isRegistered, () => {
    //   this.setData({
    //     isRegistered
    //   });
    // });
    wx.navigateTo({
      url: '/pages/login/login',
    })
  },
  onTapInterest: function() {
    const isInterested = !this.data.isInterested;
    // toggleRegister(this.data.id, isInterested, () => {
      this.setData({
        isInterested
      });
    // });
  }
})
