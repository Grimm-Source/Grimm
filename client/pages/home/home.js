//home.js
//获取应用实例
const app = getApp()

Page({
  data: {
  },
  //事件处理函数
  onLoad: function () {

  },
  bindTapProfile: function(){
    wx.navigateTo({
        url: '../profile/profile',
    })
  }
})
