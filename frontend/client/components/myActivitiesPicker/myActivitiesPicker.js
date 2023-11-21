// components/myActivitiesPicker/myActivitiesPicker.js
const { getMyActivities } = require('../../utils/requestUtil.js');

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    selectedIdx: {
      type: Number,
      value: 0,
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    myActivitiesTab: [
      { 'idx': '0', 'tabName': '我的活动'},
      { 'idx': '1', 'tabName': '已报名'},
      { 'idx': '2', 'tabName': '感兴趣'}]
  },

  /**
   * 组件的方法列表
   */
  methods: {
    myActivitiesTabClick(e) {
      const targetIdx = e.currentTarget.dataset.param;
      // this.setData({
      //   selectedIdx: targetIdx
      // });
      // refresh list
      this.triggerEvent('myActivitiesSelectedIdx', { selectedIdx: targetIdx});
    }
  }
})
