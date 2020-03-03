//获取应用实例
const { getActivityList, getRegisteredActivityList } = require('../../utils/requestUtil.js');

const app = getApp()

Page({
  data: {
    activities:[]
  },
  
  onLoad: function (options) {
  },

  onShow: function () {
    getActivityList((res) => {
      this.setData({ activities: res });
    })
  }
  
})
