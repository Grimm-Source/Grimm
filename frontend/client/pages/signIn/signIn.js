// pages/signIn/signIn.js
const {
  getActivityDetail,
  signUP,
  signOff
} = require('../../utils/requestUtil.js');
const formatTimeline = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].join('-') + ' ' + [hour, minute, second].join(':')
}

Page({

  /**
   * Page initial data
   */
  data: {
    isShowCoedSignIn:false
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (option) {
    this.setData({
      id: option.id || 4
      // id: option.id || 'om6834wZ1F35GaThbf8ZitBnzhUc'
    });
  },

  /**
   * Lifecycle function--Called when page is initially rendered
   */
  onReady: function () {
    let that = this
    wx.getLocation({
      type: 'wgs84',
      isHighAccuracy: true,
      success(res) {
        const latitude = res.latitude
        const longitude = res.longitude
        const speed = res.speed
        const accuracy = res.accuracy
      
        that.setData({
          latitude,
          longitude
        })
      }
    })

  },

  /**
   * Lifecycle function--Called when page show
   */
  onShow: function () {
    this.getActivity();
  },

  getActivity: function () {
    getActivityDetail(this.data.id, (res) => {
      const startTime = new Date(res.start_time).getTime()
      const nowTime = new Date().getTime()
      const lastMinutes = Math.floor((startTime - nowTime) / (1000 * 60))
      // console.log(startTime, nowTime, lastMinutes)

      this.setData({
        title: res.title,
        lastMinutes: lastMinutes,
        isLike: res.thumbs_up === 1,
        isRegistered: res.registered === 1,
        isInterested: res.interested === 1,
        address: res.location,
        current_state: res.current_state

      })
      //console.log(res);
    });
  },
  signUp: function (token) {
    let time = formatTimeline(new Date())
    // console.log("time:", time)
    return signUP({
      activity_id: Number(this.data.id),
      signup_time: time,
      signup_latitude: this.data.latitude,
      signup_longitude: this.data.longitude,
      sign_in_token: token
    }, (res) => {
      // console.log("res------", res)
      if (res.status === "success") {
        wx.showToast({
          title: '签到成功',
          icon: 'success',
          duration: 2500,
          success: wx.switchTab({
            url: '../home/home',
          })
        });
      }
    }, (err) => {
      wx.showModal({
        showCancel: false,
        title: '更新失败',
        content: err || "网络失败，请稍候再试"
      });
    })
  },
  signOff: function () {
    let time = formatTimeline(new Date())
    // console.log("time:", time)
    signOff({
      activity_id: Number(this.data.id),
      signoff_time: time,
      signoff_latitude: this.data.latitude,
      signoff_longitude: this.data.longitude,
    }, (res) => {
      wx.showToast({
        title: '签退成功',
        icon: 'success',
        duration: 4500,
        success: wx.switchTab({
          url: '/pages/home/home',
        })
      });
    }, (err) => {
      wx.showModal({
        showCancel: false,
        title: '更新失败',
        content: err || "网络失败，请稍候再试"
      });
    })
  },
  showCoedSignIn:function(){
    this.setData({
      isShowCoedSignIn:!this.data.isShowCoedSignIn
    })
  }
})