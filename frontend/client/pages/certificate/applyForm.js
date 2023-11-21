// pages/certificate/applyForm.js
const {
  submitCertificatectivity
} = require('../../utils/requestUtil.js');



function showMessage(message) {
  wx.showToast({
    title: message,
    icon: 'error', //error
    duration: 2000
  });
}

Page({

  /**
   * 页面的初始数据
   */
  data: {
    extendChecked: true,
    applyData: {},
    idTypeArr: ['身份证', '驾驶证']
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

  onCheck(e) {
    this.setData({
      extendChecked: e.detail.checked,
    })
  },
  bindInputChange: function (e) {
    let applyData = this.data.applyData,
    key = e.currentTarget.dataset['infoKey'];
    applyData[key] = e.detail && e.detail.value || "";
    this.setData({
      applyData
    });
  },

  validate: function(values){
    const {
      applyData = {}
    } = this.data;
    const {
      real_name,
      id_type,
      idcard,
      email,
      recipient_name,
      recipient_address,
      recipient_phone
    } = applyData
    if (!real_name) {
      showMessage('请填写真实姓名');
      return false;
    }
    if (!id_type) {
      showMessage('请选择证件类型');
      return false;
    }
    if (!idcard) {
      showMessage('请填写证件号码');
      return false;
    }
    if (!email) {
      showMessage('请输入有效电子邮箱');
      return false;
    }
    if (this.data.extendChecked) {
      if (!recipient_address) {
        showMessage('请填写收件人姓名');
        return false;
      }
      if (!recipient_name) {
        showMessage('请填写您的收件地址');
        return false;
      }
      if (!recipient_phone) {
        showMessage('请填写您的收件电话');
        return false;
      }
    }
    return true;
  },
  onSubmit: function (e) {
    if(!this.validate()){
      return;
    }
    wx.showLoading({
      title: '证书生成中...',
    })
    submitCertificatectivity(
      {
        activity_id:  wx.getStorageSync('cer_acc_list'),
        participant_openid:  wx.getStorageSync('participant_openid'),
        ...this.data.applyData,
        id_type: this.data.idTypeArr[this.data.applyData.id_type],
      },
      (res) => {
        wx.hideLoading({
          success: () => {
            wx.navigateTo({
              url: '/pages/certificate/applyList',
            });
          },
        })
      },
      (fail) => {
        wx.hideLoading({
          success: (res) => {
            wx.showToast({
              title: fail || '证书生成失败, 请稍后再试',
              icon: 'none', //error
              duration: 2000
            });
            // wx.navigateTo({
            //   url: '/pages/certificate/applyList',
            // });
          },
        })
      }
    );
  }
})
