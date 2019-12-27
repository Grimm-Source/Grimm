const {getProfile, postRegisteredActivityList} = require('../../utils/requestUtil.js');

Page({
  data: {
    apply: {},
    activityId: null,
    role: null
  },
  //事件处理函数
  onLoad: function (option) {
    if(!option.activityId){
      return;
    }
    this.setData({
        activityId: option.activityId
    });
    this.getContactInfo();
  }, 
  getContactInfo: function (){
    getProfile((res)=>{
        this.setData({
          apply: {
              tel: res.linktel,
              address: res.linkaddress,
              needPickUp: false,
              toPickUp: false
          },
          role: res.role
        })
    }); 
  },
  onTapSubmit: function(){
    let obj = {
        activityId: this.data.activityId,
        ...this.data.apply
    };
    if(this.data.role === "视障人士"){
        delete obj["toPickUp"];
    }else{
        delete obj["needPickUp"];
    }

    postRegisteredActivityList([obj],()=>{
        wx.navigateTo({
            url: '/pages/activityDetail/activityDetail?activityId='+ this.data.activityId
        })
    },()=>{

    });
  },
  checkboxChange: function (e) {
        let apply = this.data.apply;
        if(this.data.role === "视障人士"){
            apply["needPickUp"] = !apply["needPickUp"]   
        }else{
            apply["toPickUp"] = !apply["toPickUp"]
        }
        this.setData({apply})
  }
})
