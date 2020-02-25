// components/activitiesList/activitiesList.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    activities: [
      { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', 'description': '招募陪走志愿者', 'joined': '12', 'inserted': '21' },
      { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', 'description': '招募陪走志愿者', 'joined': '12', 'inserted': '21' }],
  },

  /**
   * 组件的方法列表
   */
  methods: {
    onTapActivity: function (event) {
      wx.navigateTo({
        url: '/pages/activityDetail/activityDetail?id=1',
      })
    }
  }
})
