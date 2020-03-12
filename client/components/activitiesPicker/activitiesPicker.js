// components/activitiesPicker/activitiesPicker.js
const { getActivityList, getFilteredActivities, getActivityTypes} = require('../../utils/requestUtil.js');

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    categories: {
      type: Array,
      value: [],
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    activityTimes: [
      { 'time_id': -1, 'description': '全部'},
      { 'time_id': 0, 'description': '最新' },
      { 'time_id': 1, 'description': '周末' },
      { 'time_id': 2, 'description': '最近一周' },
      { 'time_id': 3, 'description': '选择日期' },],
    activeCategory: -1,
    activeTime: -1,
  },

  pageLifetimes: {
    show: function () {
      getActivityTypes((res) => {
        this.setData({ categories: [{ tag_id: -1, tag_name: "全部" }].concat(res) })
      });

    },
  },

  /**
   * 组件的方法列表
   */
  methods: {
    _initTimeFilter: function() {
      for (let index = 0; index < this.data.activeTime.length; index++) {

      }
    },

    filterParamsChange: function(activeCategory, activeTime) {
      this.triggerEvent('myEvent', {
        category: this.data.activeCategory,
        time: this.data.activeTime,
      }, {})
    },

    tapCategory: function (event) {
      this.setData({
        activeCategory: event.currentTarget.id,
      });
      this.filterParamsChange();
    },

    tapTime: function (event) {
      this.setData({
        activeTime: event.currentTarget.id,
      });
      this.filterParamsChange();
    },
  },
})
