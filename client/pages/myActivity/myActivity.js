// // pages/myActivity/myActivity.js

Page({
  data: {
    selectedIdx: 0,
    
  },

  onLoad: function (options) {
  },

  handleMyActivitiesPickerEvent: function (event) {
    this.setData({
      selectedIdx: event.detail.selectedIdx
    })
  },

})

