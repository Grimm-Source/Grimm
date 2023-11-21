const {getCarousel} = require('../../utils/requestUtil.js');

Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    swiperItems: [{title: "欢迎使用", url: "", photo_url: ""}]
  },

  /**
   * 组件的方法列表
   */
  methods: {
    getData(){
      getCarousel((res)=>{
        this.setData({
          swiperItems: res
        });
      }, (res)=>{

      });
    },
    onTapItem(e){
      // TODO：add external links
      // if(!e.currentTarget.dataset.param ){
      //   return;
      // }
      // wx.navigateTo({
      //   url: "/pages/tips/tips"
      // });
    }
  }
})
