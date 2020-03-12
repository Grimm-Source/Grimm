//获取应用实例
const { getActivityList, getActivityTypes } = require('../../utils/requestUtil.js');

const app = getApp()

Page({
  data: {
    activityCategories: [],
    activities:[],
    needShowTabbar: true,
    showTabbarText: "隐藏",
  },
  
  onLoad: function (options) {
  },

  onShow: function () {
    this.selectComponent(".home-tips-siwper").getData();
  },

  toggleTabbar: function() {
    this.setData({
      needShowTabbar: !this.data.needShowTabbar,
      showTabbarText: this.data.needShowTabbar ? "隐藏" : "显示"
    });

    if (!this.data.needShowTabbar) {
      wx.hideTabBar();
    } else {
      wx.showTabBar();
    }
  },

  showPersonInfo: function() {
    wx.navigateTo({
      url: "/pages/personalNoTab/personal",
      fail: function(res) {
        console.log(res);
      }
    });
  }
  
})
