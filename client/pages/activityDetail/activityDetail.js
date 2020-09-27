const { getActivityDetail, toggleInterest, toggleThumbsUp, toggleRegister, shareActivity} = require('../../utils/requestUtil.js');

const app = getApp();

Page({
  data: {
    banner: '/images/banner.jpeg',
    title: '',
    isLike: false,
    start_time: '',
    date: '',
    address: '',
    content: '',
    isRegistered: false,
    isInterested: false,
    volunteerTotal: 0,
    volunteerCurr: 0,
    visuallyImpairedTotal: 0,
    visuallyImpairedCurr: 0,
    isActivityEnd: false,
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
    if( !app.globalData.isAuthorized){
      this.authorize();
      return;
    }
    const isLike = !this.data.isLike;
    toggleThumbsUp(this.data.id, isLike, () => {
      this.setData({
        isLike
      });
    });
  },
  getActivity: function (){
    getActivityDetail(this.data.id, (res) => {
      const startTime = res.start_time.replace("T", " ");
      const endTime = res.end_time.replace("T", " ");
      const isStarted = Date.now() > Date.parse(res.start_time);
      this.setData({
        title: res.title,
        isLike: res.thumbs_up === 1,
        isRegistered: res.registered === 1,
        isInterested: res.interested === 1,
        isActivityEnd: isStarted,
        start_time: res.start_time,
        date: `${startTime} 至 ${endTime}`,
        address: res.location,
        volunteerTotal: res.volunteer_capacity,
        volunteerCurr: res.registered_volunteer,
        visuallyImpairedTotal: res.vision_impaired_capacity,
        visuallyImpairedCurr: res.registered_impaired,
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
  onShareAppMessage:function(){
    shareActivity(this.data.id);
  },
  onTapRegister: function() {
    if( !app.globalData.isAuthorized){
      this.authorize('login');
      return;
    }
    const isRegistered = !this.data.isRegistered;//activity
    if( app.globalData.isRegistered ){ // user
      if (this.checkActivityStarted()) {
        console.log("用户点击已开始活动.");
        return;
      }

      const isVolunteer =  app.globalData.isVolunteer; 
      toggleRegister(this.data.id, isRegistered, () => {
        if(isVolunteer){
          this.setData({
            isRegistered,
            volunteerCurr: this.updateCurrentValue(isRegistered, true)
          });
          if(isRegistered){
            wx.showModal({
              title: '报名成功',
              showCancel: false
            });
          } else{
            wx.showModal({
              title: '报名取消',
              showCancel: false
            });
          }
          return;
        }
        this.setData({
          isRegistered,
          visuallyImpairedCurr: this.updateCurrentValue(isRegistered, false)
        });        
      });

      return;
    }
    wx.navigateTo({
      url: '/pages/login/login',
    });
  },
  onTapInterest: function() {
    if( !app.globalData.isAuthorized){
      this.authorize();
      return;
    }
    const isInterested = !this.data.isInterested;
    toggleInterest(this.data.id, isInterested, () => {
      this.setData({
        isInterested
      });
    });
  },
  
  authorize: function(redirectPage, params){
    const page = redirectPage || `activityDetail&value=${this.data.id}&key=id`;
    wx.navigateTo({
      url: `/pages/authorize/authorize?redirectPage=${page}` 
    });
  },

  checkActivityStarted: function() {
    if (this.data.start_time == '') return false;
    
    const isStarted = Date.now() > Date.parse(this.data.start_time);
    if (isStarted) {
      wx.showModal({
        showCancel: false,
        title: '活动已开始',
        content: "您想操作的活动已开始，请选择还未开始的活动，谢谢!"
      });
    }
  },

  updateCurrentValue: function(isRegistered, isVolunteer) {
    var updatedCurr = 0;
    if (isVolunteer && this.data.volunteerCurr) {
      updatedCurr = this.data.volunteerCurr;
    } else if (!isVolunteer && this.data.visuallyImpairedCurr){
      updatedCurr = this.data.visuallyImpairedCurr;
    }

    if (isRegistered) {
      updatedCurr++;
    } else if (updatedCurr > 0) {
      updatedCurr--;
    }
    return updatedCurr;
  }
})
