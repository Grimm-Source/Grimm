// components/activitiesList/activitiesList.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    activitiesProp: {
      type: Array,
      value:[],
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
  },

  /**
   * 组件的方法列表
   */
  methods: {
    onTapActivity: function (event) {
      wx.navigateTo({
        url: '/pages/activityDetail/activityDetail?id=1',
      })
    },
    
    onPulling: function() {
      
    }
  }
})
