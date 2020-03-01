// components/myActivitiesPicker/myActivitiesPicker.js
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
    myActivitiesTab: [
      { 'idx': '0', 'tabName': '全部'},
      { 'idx': '1', 'tabName': '已报名'},
      { 'idx': '2', 'tabName': '感兴趣'},
      { 'idx': '3', 'tabName': '已结束活动'},],

    selectedIdx: 0
  },

  /**
   * 组件的方法列表
   */
  methods: {
    // myActivitiesTabClick(e) {
    //   const targetIdx = e.currentTarget.dataset.param;
    //   this.setData({
    //     selectedIdx: targetIdx
    //   });
    //   // refresh list
    // }

    
  }
})
