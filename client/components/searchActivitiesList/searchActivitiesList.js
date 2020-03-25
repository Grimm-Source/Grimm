// components/searchActivitiesList/searchActivity.js
Component({
  /**
   * Component properties
   */
  properties: {
    searchedActivities: {
      type: Array,
      observer: function (searchedActivities) {
        this.setData({
          searchedActivities: searchedActivities,
          ifSearched: true
        })
      }
    }
  },

  data: {
    searchedActivities: null,
    ifSearched: false
  },

  lifetimes: {
    attached: function() {
      // 在组件实例进入页面节点树时执行
      this.setData({
        ifSearched: false
      })
    }
  },

  /**
   * Component methods
   */
  methods: {
    onTapActivity: function(e){
      let item = e.currentTarget.dataset && e.currentTarget.dataset.item,
      activityId = item.id;
      wx.navigateTo({
          url: '/pages/activityDetail/activityDetail?activityId='+ activityId,
      })
    }
  }
})
