// pages/register/register.ts
import Toast from '@vant/weapp/toast/toast'
const { request } = require('../../utils/request')
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    avatarUrl: '',
    phone: '',
    roleShow: ['视障者', '志愿者'],
    roleIndex: 0, // 0:impaired 1:volunteer
    role: 'impaired', // impaired, volunteer
    name: '',
    genderShow: ['男', '女'],
    genderIndex: 0,
    gender: '男',
    email: '',
    birthdate: '',
    region: '',
    linkaddress: '',
    idcard: '',
    disabledID: '',
    emergencyPerson: '',
    emergencyTel: '',
    usercomment: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      phone: options.phone
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  async onSubmitTap() {
    try {
      const { avatarUrl, phone, role, name, gender, email, birthdate, region, linkaddress, idcard } = this.data
      const params = { avatarUrl, phone, role, name, gender, email, birthdate, linkaddress, idcard }
      if (this._verify(name, email, birthdate, region, idcard)) {
        Toast.loading({ message: '加载中...', forbidClick: true, duration: 0 })
        const res = await request('register', 'POST', params)
        if (res.status === 'success') {
          wx.showModal({
            title: '',
            content: '注册成功，欢迎加入',
            showCancel: false,
            success: (res) => {
              if (res.confirm) {
                wx.navigateBack({
                  delta: 1
                })
              }
            }
          })
        } else if (res.message === '用户已注册，请登录') {
          wx.showModal({
            title: '',
            content: '用户已注册，请直接登录',
            showCancel: false,
            success: (res) => {
              if (res.confirm) {
                wx.navigateBack({
                  delta: 1
                })
              }
            }
          })
        } else {
          Toast.fail(res.message)
        }
      }
    } catch (error) {
      console.error('请求失败：', error)
    }
  },

  _verify(name, email, birthdate, region, idcard) {
    if (name === '') {
      wx.showModal({ title: '错误提示', content: '请填写真实姓名', showCancel: false })
      return false
    }
    const emailReg = /^[A-Za-z0-9]+([-_.][A-Za-z0-9]+)*@([A-Za-z0-9]+[-.])+[A-Za-zd]{2,5}$/
    if (email === '') {
      wx.showModal({ title: '错误提示', content: '请填写电子邮箱', showCancel: false })
      return false
    } else if (email && !emailReg.test(email)) {
      wx.showModal({ title: '错误提示', content: '请填写正确的邮箱地址', showCancel: false })
      return false
    }
    if (birthdate === '') {
      wx.showModal({ title: '错误提示', content: '请选择出生日期', showCancel: false })
      return false
    }
    if (region === '') {
      wx.showModal({ title: '错误提示', content: '请选择所在城区', showCancel: false })
      return false
    }
    var idReg = /^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10|11|12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx]$/
    if (idcard === '') {
      wx.showModal({ title: '错误提示', content: '请填写身份证号', showCancel: false })
      return false
    }
    // } else if (idcard && !idReg.test(idcard)) {
    //   wx.showModal({ title: '错误提示', content: '请填写正确的身份证号', showCancel: false })
    //   return false
    // }
    return true
  },

  onChooseAvatar(e) {
    this.setData({
      avatarUrl: e.detail.avatarUrl
    })
  },

  changeNameInput(e) {
    this.setData({
      name: e.detail.value
    })
  },

  changeRoleSelect(e) {
    this.setData({
      roleIndex: e.detail.value,
      role: e.detail.value === '0' ? 'impaired' : 'volunteer'
    })
  },

  changeGenderSelect(e) {
    this.setData({
      genderIndex: e.detail.value,
      gender: e.detail.value === '0' ? '男' : '女'
    })
  },

  changeEmailInput(e) {
    this.setData({
      email: e.detail.value
    })
  },

  changeBirthdateSelect(e) {
    this.setData({
      birthdate: e.detail.value
    })
  },

  changeRegionSelect(e) {
    this.setData({
      region: e.detail.value,
      linkaddress: e.detail.value.join(',')
    })
  },

  changeIdcardInput(e) {
    this.setData({
      idcard: e.detail.value
    })
  },

  changeEmergencyPersonInput(e) {
    this.setData({
      emergencyPerson: e.detail.value
    })
  },

  changeEmergencyTelInput(e) {
    this.setData({
      emergencyTel: e.detail.value
    })
  },

  changeUsercommentInput(e) {
    this.setData({
      usercomment: e.detail.value
    })
  },
})


