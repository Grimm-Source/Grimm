// // pages/myActivity/myActivity.js

const myActivitiesType = {
  MYALL: 0,
  REGISTERED: 1,
  INTERESTED: 2
};

Page({
  data: {
    selectedIdx: myActivitiesType.MYALL,
  },

  //事件处理函数
  onLoad: function (options) {
    this._setSelectedIdx(options.type);
  }, 

  handleMyActivitiesPickerEvent: function (event) {
    this._setSelectedIdx(event.detail.selectedIdx)
  },

  _setSelectedIdx: function(selectedType) {
    this.setData({
      selectedIdx: selectedType
    });
  }

})

