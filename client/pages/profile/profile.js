import WxValidate from "../../utils/WxValidate";
const {getVerifyCode, verifyCode, getProfile, updateProfile} = require('../../utils/requestUtil.js');

const app = getApp()

Page({
  
  data: {
    meta:{
      genderArray: ["男","女"],
      birthdayStartDate: "1910-01-01",
      birthdayEndDate: (new Date).toJSON().split("T")[0],
    }
  },

  onShow: function (options) {
    this.__initData();
    this.__getProfile();
  },

  updateProfile: function(e){
    if(!this.data.ui.isFormValid){
      return;
    }
    this.__updateProfile();
  },

  getCode: function(e){
    getVerifyCode(this.data.userInfo.tel);
    this.__setUis({
      "isCodeSent": true,
      "telNeedValidate": this.data.userInfo.tel 
    });
    this.__updateTimer();
  },

  validateCode: function(){
    if(this.data.ui.telNeedValidate !== this.data.userInfo.tel){ //incase the user change the number after get a code
      wx.showToast({
        title: '验证失败',
        icon: 'success', //error
        duration: 2000
      });
    }
    verifyCode({ 
      tel: this.data.userInfo.tel, 
      code: this.data.code
    },()=>{
        wx.showToast({
          title: '验证成功',
          icon: 'success', //error
          duration: 2000
        });
        this.__setUi("isTelValid", true);
        this.__setError("tel", false);
    },()=>{
      wx.showToast({
        title: '验证码错误',
        icon: 'success', //error
        duration: 2000
      });
    });
  },

  bindTelChange: function(e){
    if((e.detail && e.detail.value) === this.data.userInfo.tel){
      return;
    }
    this.__setUis({
      "isTelChanged": true,
      "isTelValid": false
    });
    this.setData("code", "");
    this.__updateUserInfo("tel", e.detail && e.detail.value);
  },

  bindCodeChange: function(e){
    this.setData("code", e.detail && e.detail.value);
  },

  bindGenderChange: function(e){
    this.__updateUserInfo("gender", this.data.meta.genderArray[e.detail && Number(e.detail.value)]);
  },

  bindDateChange: function(e){
    this.__updateUserInfo("birthDate", e.detail && e.detail.value);
  },
  bindLinktelChange: function(e){
    this.__updateUserInfo("linktel", e.detail && e.detail.value);
  },
  bindLinkaddressChange: function(e){
    this.__updateUserInfo("linkaddress", e.detail && e.detail.value);
  },
  bindEmergencyPersonChange: function(e){
    this.__updateUserInfo("emergencyPerson", e.detail && e.detail.value);
  },
  bindEmergencyTelChange: function(e){
    this.__updateUserInfo("emergencyTel", e.detail && e.detail.value);
  },

  __initData: function(){
    this.setData({
      code:"",
      ui:{
          isTelChanged: false,
          leftTimeLabel: "获取验证码",
          isCodeSent: false,
          isTelValid: true,
          telNeedValidate: null,
          isFormValid: true,
          isLoadingValid: false,
          isLoadingUpdate: false
      },
      error: {
        tel: false,
        linkaddress: false,
        linktel: false,
        emergencyPerson: false,
        emergencyTel: false,
      }
    });
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
      case "emergencyPerson":
          if(this.data.userInfo.role !== "视障人士"){
            return true;
          }
          return !!value && (value.length <= 20);
      case "tel":
        return !!value && mobile.test(value) && this.data.ui.isTelValid;
      case "emergencyTel":
        if(this.data.userInfo.role !== "视障人士"){
          return true;
        }
      case "linktel":
        return !!value && (mobile.test(value) || phone.test(value));
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
          wx.switchTab({
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
    },(err)=>{
      wx.showModal({
        showCancel: false,
        title: '更新失败',
        content: err || "网络失败，请稍候再试"
      });  
    });
  }
})