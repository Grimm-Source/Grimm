import WxValidate from "../../utils/WxValidate";
const {getVerifyCode, verifyCode, getProfile, updateProfile} = require('../../utils/requestUtil.js');

const app = getApp()

Page({

  /**
   * Page initial data
   */
  data: {
    id: "11111111111", //temp openid 
    meta:{
        genderArray: ["男","女"],
        birthdayStartDate: "1910-01-01",
        birthdayEndDate: (new Date).toJSON().split("T")[0],
    },
    ui:{
        isMobileChanged: false,
        leftTimeLabel: "获取验证码",
        isCodeSent: false,
        isMobileValid: true,
        mobileNeedValidate: null,
        code: "",
        isFormValid: true,
        isLoadingValid: false,
        isLoadingUpdate: false
    },
    error: {
      nickName: false,
      mobile: false,
      address: false,
      phone: false,
      emergencyName: false,
      emergencyPhone: false,
    }
  },
  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {
    this.__getProfile();
  },

  updateProfile: function(e){
    if(!this.data.ui.isFormValid){
      return;
    }
    this.__updateProfile();
  },

  getCode: function(e){
    getVerifyCode(this.data.userInfo.mobile);
    this.__setUi("isCodeSent", true);
    this.__updateTimer();
  },

  validateCode: function(){
    verifyCode({ 
      mobile: this.data.userInfo.mobile, 
      code: this.data.ui.code
    },()=>{
      if(this.ui.mobileNeedValidate !== this.userInfo.phone){ //incase the user change the number after get a code
        wx.showToast({
          title: '手机号不匹配，请重新获取',
          icon: 'success', //error
          duration: 2000
        });
      }else{
        wx.showToast({
          title: '验证成功',
          icon: 'success', //error
          duration: 2000
        });
        this.__setUi("isMobileValid", true);
        this.__setError("mobile", false);
      }
    },()=>{
      wx.showToast({
        title: '验证码错误',
        icon: 'success', //error
        duration: 2000
      });
    });
  },

  bindNickNameChange: function(e){
    this.__updateUserInfo("nickName", e.detail && e.detail.value);
  },

  bindMobileChange: function(e){
    if((e.detail && e.detail.value) === this.data.userInfo.mobile){
      return;
    }
    this.__setUis({
      "isMobileChanged": true,
      "isMobileValid": false,
      "code": null,
      "mobileNeedValidate": e.detail.value 
    });
    this.__updateUserInfo("mobile", e.detail && e.detail.value);
  },

  bindCodeChange: function(e){
    this.__setUi("code", e.detail && e.detail.value);
  },

  bindGenderChange: function(e){
    this.__updateUserInfo("gender", e.detail && Number(e.detail.value));
  },

  bindDateChange: function(e){
    this.__updateUserInfo("birthday", e.detail && e.detail.value);
  },
  bindPhoneChange: function(e){
    this.__updateUserInfo("phone", e.detail && e.detail.value);
  },
  bindAddressChange: function(e){
    this.__updateUserInfo("address", e.detail && e.detail.value);
  },
  bindEmergencyNameChange: function(e){
    this.__updateUserInfo("emergencyName", e.detail && e.detail.value);
  },
  bindEmergencyPhoneChange: function(e){
    this.__updateUserInfo("emergencyPhone", e.detail && e.detail.value);
  },

  __updateUserInfo: function(key, value = null, isIgnoreValid){
    let userInfo = this.data && this.data.userInfo;
    userInfo[key] = value;
    this.setData({
        userInfo
    });
    if(!isIgnoreValid && !this.__validate(key, value)){
      this.__setUi("isFormValid", false);
      this.__setError(key, true);
    }else{
      this.__validateAll();
    }
  },

  __setUi: function(key, value){
    let ui = this.data && this.data.ui;
      ui[key] = value;
      this.setData({
        ui
      });
  },
  __setError: function(key, value){
    let error = this.data && this.data.error;
      error[key] = value;
      this.setData({
        error
      });
  },

  __setUis: function(obj){
    for(let key in obj){
      this.__setUi(key, obj[key]);
    }
  },

  __validate: function(key, value){
    let mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/,
    phone = /^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$/;
    switch(key) {
      case "emergencyName":
          if(this.data.userInfo.userType !== "normal"){
            return true;
          }
      case "nickName":
        return !!value && (value.length <= 20);
      case "mobile":
        return !!value && mobile.test(value) && this.data.ui.isMobileValid;
      case "emergencyPhone":
        if(this.data.userInfo.userType !== "normal"){
          return true;
        }
      case "phone":
        return !!value && (mobile.test(value) || phone.test(value));
      case "gender":
        return value === 0 || value === 1;
      default:
        return !!value
    }
  },

  __validateAll: function(){
    let isValidate = true;
    for(let key in this.data.userInfo){
      if(!this.__validate(key, this.data.userInfo[key])){
        isValidate = false;
        this.__setError(key, true);
      }else{
        this.__setError(key, false);
      }
    }
    this.__setUi("isFormValid", isValidate);
  },

  __updateTimer: function(){
    let that = this,
    time = 60,
    timer = setInterval(function(){
      that.__setUi("leftTimeLabel", `${time--}秒后再试`);
      if(time < 0){
        time = 60;
        clearInterval(timer);
        that.__setUi("isCodeSent", false);
        that.__setUi("leftTimeLabel", `获取验证码`);
      }
    }, 1000);
  },

  __getProfile: function(){
    return getProfile(this.data.id, (data) => {
      this.setData({
        userInfo: data
      });
    },(err) => {
      wx.showModal({
        title: '提示',
        content: err,
        showCancel: false,
        success () {
          wx.navigateTo({
            url: '../home/home',
          });
        }
      });     
    });
  },

  __updateProfile: function(){
    return updateProfile(this.data.userInfo, (res)=>{
      wx.showToast({
        title: '已更新',
        icon: 'success',
        duration: 300
      });
      setTimeout(function(){
        wx.navigateTo({
          url: '../home/home',
        });
      }, 300);
    },(err)=>{
      wx.showModal({
        showCancel: false,
        title: '更新失败',
        content: err || "网络失败，请稍候再试"
      });  
    });
  }
})