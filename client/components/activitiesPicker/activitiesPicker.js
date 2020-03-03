// components/activitiesPicker/activitiesPicker.js
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
    activityCategories: [
      { 'type': '0', 'categoryName': '全部' },
      { 'type': '1', 'categoryName': '学习' },
      { 'type': '2', 'categoryName': '分享' },
      { 'type': '3', 'categoryName': '娱乐' },
      { 'type': '4', 'categoryName': '运动' },
      { 'type': '5', 'categoryName': '心理疏导' },
      { 'type': '6', 'categoryName': '其他活动' },],
    activityTimes: [
      { 'time': '0', 'description': '全部' },
      { 'time': '1', 'description': '最新' },
      { 'time': '2', 'description': '周末' },
      { 'time': '3', 'description': '最近一周' },
      { 'time': '4', 'description': '选择日期' },],
    activeType: 0,
    activeTime: 0,
  },

  /**
   * 组件的方法列表
   */
  methods: {
    tapCategory: function (event) {
      this.setData({
        activeType: event.currentTarget.id,
      })

    },

    tapTime: function (event) {
      this.setData({
        activeTime: event.currentTarget.id,
      })
    },

    requestFilteredActivities: function() {
      // get activities by type and time
    }
  },
})
