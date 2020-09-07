// // pages/myActivity/myActivity.js

Page({
  data: {
    selectedIdx: 0,
    
  },

  onLoad: function (options) {
    this.setData({
      selectedIdx: parseInt(options.selectedIdx)
    })
  },

  handleMyActivitiesPickerEvent: function (event) {
    this.setData({
      selectedIdx: parseInt(event.detail.selectedIdx)
    })
  },

})

