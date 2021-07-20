const {
  getActivityDetail,
  toggleInterest,
  toggleThumbsUp,
  toggleRegister,
  shareActivity
} = require('../../utils/requestUtil.js');

const apiUrl = require('../../config.js').apiUrl;

const app = getApp();

Page({
  data: {
    banner: '',  ///images/banner.jpeg
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

    pickupImpairedModalVisible: false, //弹出 不需要、晚些决定、需要接送 模态框
    needPickup: false, //需要接送
    themePicName: '',
    impired: {
      name: '',
      idNo: '',
      impairedNo: '',
      pickupAddr: '',
      emergencyContact: '',
    },
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
  onTapLike: function () {
    if (!app.globalData.isAuthorized) {
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
  getActivity: function () {
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
        date: `${startTime.substr(0, 16)} 至 ${endTime.substr(0,16)}`,
        address: res.location,
        volunteerTotal: res.volunteer_capacity,
        volunteerCurr: res.registered_volunteer,
        visuallyImpairedTotal: res.vision_impaired_capacity,
        visuallyImpairedCurr: res.registered_impaired,
        needPickup: res.needPickup == 1,
        banner: apiUrl + '/activity/themePic?activity_them_pic_name=' + res.activity_them_pic_name,
        impired: {
          name: res.name,
          idNo: res.idNo,
          impairedNo: res.impairedNo,
          pickupAddr: res.pickupAddr,
          emergencyContact: res.emergencyContact,
        },
        content: `
          ${res.content}

          [注意事项]
          ${res.notice}

          [其他]
          ${res.others}
        `
      })
      //console.log(res);
    });
  },
  onShareAppMessage: function () {
    shareActivity(this.data.id);
  },
  onTapRegister: function () {
    if (!app.globalData.isAuthorized) {
      this.authorize('login');
      return;
    }
    const isRegistered = !this.data.isRegistered; //activity
    if (app.globalData.isRegistered) { // user registered
      if (this.checkActivityStarted()) {
        console.log("用户点击已开始活动.");
        return;
      }
      const isVolunteer = app.globalData.isVolunteer;

      /* check the capacity before register activity request */
      var capacity_allow = true;
      if (isVolunteer) {
        if (this.data.volunteerCurr >= this.data.volunteerTotal) {
          capacity_allow = false;
        }
      } else {
        if (this.data.visuallyImpairedCurr >= this.data.visuallyImpairedTotal) {
          capacity_allow = false;
        }
      }
      if (capacity_allow || this.data.isRegistered) {
        /* register activity request */
        toggleRegister(this.data.id, isRegistered, () => {
          if (isVolunteer) {
            this.setData({
              isRegistered,
              volunteerCurr: this.updateCurrentValue(isRegistered, true)
            });
          } else { // impaired
            this.setData({
              isRegistered,
              visuallyImpairedCurr: this.updateCurrentValue(isRegistered, false)
            });
          }
          if (isRegistered) {
            if (app.globalData.isVolunteer) {
              let url = '../volunteerSignUpSuccess/volunteerSignUpSuccess?activityId=' + this.data.id + '&'
              url = url + 'title=' + this.data.title + '&'
              url = url + 'date=' + this.data.date + '&'
              url = url + 'address=' + this.data.address + '&'
              wx.navigateTo({
                url: url
              });
            } else {
              this.setData({
                pickupImpairedModalVisible: true
              });
            }
          } else {
            wx.showModal({
              title: '报名取消',
              showCancel: false
            });
          }
        },(message)=>{
          wx.showToast({
            title: message || '报名异常',
            icon: 'none',
            duration: 2000
          });
        });
      } else { // capacity not allow the register
        wx.showModal({
          title: '报名人数已满',
          showCancel: false
        });
      }
    } else { // user no register
      wx.showModal({
        title: "请先注册，再报名",
        showCancel: true,
        cancelText: "再想想",
        confirmText: "立即注册",
        success: function (res) {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/login/login',
            });
          }
        }
      });
    }
  },
  onTapInterest: function () {
    if (!app.globalData.isAuthorized) {
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

  authorize: function (redirectPage, params) {
    const page = redirectPage || `activityDetail&value=${this.data.id}&key=id`;
    wx.navigateTo({
      url: `/pages/authorize/authorize?redirectPage=${page}`
    });
  },

  checkActivityStarted: function () {
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

  updateCurrentValue: function (isRegistered, isVolunteer) {
    var updatedCurr = 0;
    if (isVolunteer && this.data.volunteerCurr) {
      updatedCurr = this.data.volunteerCurr;
    } else if (!isVolunteer && this.data.visuallyImpairedCurr) {
      updatedCurr = this.data.visuallyImpairedCurr;
    }

    if (isRegistered) {
      updatedCurr++;
    } else if (updatedCurr > 0) {
      updatedCurr--;
    }
    return updatedCurr;
  },

  onTapNotRequired: function () {
    console.log('Not required pick up.')
    this.setData({
      pickupImpairedModalVisible: false
    });
  },

  onTapDecideLater: function () {
    console.log('Will decide later.')
    this.setData({
      pickupImpairedModalVisible: false
    });
  },

  onTapNeedPickup: function () {
    console.log('Need pick up (from modal). will redirect to pick up detail page.')
    this.setData({ pickupImpairedModalVisible: false });
    let url = '../pickupImpaired/pickup?activityId=' + this.data.id + '&'
    url = url + 'title=' + this.data.title + '&'
    url = url + 'date=' + this.data.date + '&'
    url = url + 'address=' + this.data.address + '&'
    wx.navigateTo({
      url: url
    });
  },

  onTapINeedPickup: function () {
    console.log('I need pick up (from activity detail page). will redirect to pick up detail page.')
    let url = ''
    if (app.globalData.isVolunteer){
      url = url + '../pickupVolunteer/pickupVolunteer?activityId=' + this.data.id + '&'
    }else {
      url = url + '../pickupImpaired/pickup?activityId=' + this.data.id + '&'
    }
    url = url + 'title=' + this.data.title + '&'
    url = url + 'date=' + this.data.date + '&'
    url = url + 'address=' + this.data.address + '&'
    url = url + 'willPickup=1' + '&'
    wx.navigateTo({
      url: url
    });
  },

  onTapPickupDetail: function () {
    console.log('Show pick up detail.')
    let url = ''
    if (app.globalData.isVolunteer) {
      url = url + '../pickupVolunteerDetail/pickupVolunteerDetail?activityId=' + this.data.id + '&'
    }else {
      url = url + '../pickupImpaired/pickup?activityId=' + this.data.id + '&'
      url = url + 'name=' + this.data.impired.name + '&'
      url = url + 'idNo=' + this.data.impired.idNo + '&'
      url = url + 'impairedNo=' + this.data.impired.impairedNo + '&'
      url = url + 'pickupAddr=' + this.data.impired.pickupAddr + '&'
      url = url + 'emergencyContact=' + this.data.impired.emergencyContact + '&'
    }
    url = url + 'title=' + this.data.title + '&'
    url = url + 'date=' + this.data.date + '&'
    url = url + 'address=' + this.data.address + '&'
    wx.navigateTo({
      url: url
    });
  },
})