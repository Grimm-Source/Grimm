// pages/certificate/applyForm.js
const {
  submitCertificatectivity
} = require('../../utils/requestUtil.js');
Page({

  /**
   * 页面的初始数据
   */
  data: {
    extendChecked: true,
    applyData:{}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  
  onCheck(e){
    this.setData({
      extendChecked: e.detail.checked,
    }) 
  },
  bindInputChange: function(e){
    let applyData = this.data.applyData,
    key = e.currentTarget.dataset['infoKey'];
    applyData[key] = e.detail && e.detail.value || "";
    this.setData({
      applyData
    });
  },
  onSubmit: function(e){
    const { applyData } = this.data
    submitCertificatectivity(applyData,
      (res) => {
      
      },
      (fail) => {
        wx.showToast({
          title: fail || '证书生成失败',
          icon: 'none', //error
          duration: 2000
        });
      }
    );
    console.log(applyData)
  }
})
