//app.js
const {getRegisterStatus} = require('utils/requestUtil.js');
App({
  globalData: {
    userInfo: null,
    isAuthorized: false,
    isRegistered: false,
    activityList: 
    // [
    //   {"adminId": 0, "content": "test", "duration": {"day": 1, "hour": 0, "min": 13, "sec": 0}, "end_time": "2020-04-11T12:00:00", "id": 9, "location": "Shanghai", "notice": "test", "others": "", "start_time": "2020-04-10T11:47:00", "tag": "其它,保健", "title": "test1", "isLike": true, "likeNum": 10, "isInterested": false, "volunteers": 10, "vision_impaireds": 40}, 
    //   {"adminId": 0, "content": "测试数据", "duration": {"day": 4, "hour": 0, "min": 2, "sec": 0}, "end_time": "2020-04-14T15:09:00", "id": 8, "location": "上海人民广场", "notice": "测试数据", "others": "交通安全", "start_time": "2020-04-10T15:07:00", "tag": "分享,文娱,学习", "title": "集善助盲摄影作品展", "isLike": true, "likeNum": 2,"isInterested": false, "volunteers": 10}, 
    //   {"adminId": 0, "content": "待完善", "duration": {"day": 4, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-04-02T14:12:33", "id": 4, "location": "北京王府井新燕莎金街购物广场", "notice": "待完善", "others": "", "start_time": "2020-03-29T14:12:33", "tag": "保健,其它", "title": "全新大型公益互动体验“非视觉太极”活动月", "isLike": false, "likeNum": 0, "isInterested": false}, 
    //   {"adminId": 0, "content": "阴天，宅家，吃饭睡觉打豆豆", "duration": {"day": 1, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-03-30T09:44:24", "id": 3, "location": "Beijing", "notice": "阴天，宅家，吃饭睡觉打豆豆", "others": "", "start_time": "2020-03-29T09:44:24", "tag": "分享,文娱", "title": "今天是阴天", "isLike": false, "likeNum": 6, "isInterested": false}, 
    //   {"adminId": 0, "content": "春暖花开，一起出门放风筝。", "duration": {"day": 1, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-03-27T16:29:40", "id": 2, "location": "zhejiang", "notice": "春暖花开，一起出门放风筝。", "others": "", "start_time": "2020-03-26T16:29:40", "tag": "运动,文娱,保健", "title": "今天天气好", "isLike": true, "likeNum": 20, "isInterested": false}
    // ]
    [
      {"adminId": 0, "content": "5月7日，中国人民银行、国家外汇管理局发布《境外机构投资者境内证券期货投资资金管理规定》（中国人民银行 国家外汇管理局公告〔2020〕第2号，以下简称《规定》），明确并简化境外机构投资者境内证券期货投资资金管理要求，进一步便利境外投资者参与我国金融市场。《规定》正式取消合格境外机构投资者（QFII）和人民币合格境外机构投资者（QDII）（以下简称合格投资者）境内证券投资额度管理要求，对合格投资者跨境资金汇出入和兑换实行登记管理。\n\n此外，《规定》主要内容还包括：实施本外币一体化管理，允许合格投资者自主选择汇入资金币种和时机；大幅简化合格投资者境内证券投资收益汇出手续，取消中国注册会计师出具的投资收益专项审计报告和税务备案表等材料要求，改以完税承诺函替代；取消托管人数量限制，允许单家合格投资者委托多家境内托管人，并实施主报告人制度；完善合格投资者境内证券投资外汇风险及投资风险管理要求；人民银行、外汇局加强事中事后监管。", "duration": {"day": 1, "hour": 0, "min": 30, "sec": 0}, "end_time": "2020-05-08T20:30:00", "id": 11, "location": "上海人民广场", "notice": "5月7日，中国人民银行、国家外汇管理局发布《境外机构投资者境内证券期货投资资金管理规定》（中国人民银行 国家外汇管理局公告〔2020〕第2号，以下简称《规定》），明确并简化境外机构投资者境内证券期货投资资金管理要求，进一步便利境外投资者参与我国金融市场。《规定》正式取消合格境外机构投资者（QFII）和人民币合格境外机构投资者（QDII）（以下简称合格投资者）境内证券投资额度管理要求，对合格投资者跨境资金汇出入和兑换实行登记管理。\n\n此外，《规定》主要内容还包括：实施本外币一体化管理，允许合格投资者自主选择汇入资金币种和时机；大幅简化合格投资者境内证券投资收益汇出手续，取消中国注册会计师出具的投资收益专项审计报告和税务备案表等材料要求，改以完税承诺函替代；取消托管人数量限制，允许单家合格投资者委托多家境内托管人，并实施主报告人制度；完善合格投资者境内证券投资外汇风险及投资风险管理要求；人民银行、外汇局加强事中事后监管。", "others": "交通安全", "start_time": "2020-05-07T20:00:00", "tag": "文娱", "title": "“公益365计划”正式启动", "isLike": true, "likeNum": 10, "isInterested": false, "volunteers": 10, "vision_impaireds": 40, "registered": false}, 
      {"adminId": 0, "content": "因为新冠疫情，第39届金像奖举行了史上首次线上颁奖典礼。中国香港电影金像奖协会董事局主席尔冬升通过视频直播的形式宣布获奖名单", "duration": {"day": 1, "hour": 0, "min": 13, "sec": 0}, "end_time": "2020-04-11T12:00:00", "id": 9, "location": "Shanghai", "notice": "因为新冠疫情，第39届金像奖举行了史上首次线上颁奖典礼。中国香港电影金像奖协会董事局主席尔冬升通过视频直播的形式宣布获奖名单", "others": "", "start_time": "2020-04-10T11:47:00", "tag": "其它,保健,分享,文娱,学习", "title": "test1", "isLike": true, "likeNum": 3, "isInterested": true, "volunteers": 10, "vision_impaireds": 40, "registered": false}, 
      {"adminId": 0, "content": "集团预期自投资金科股份起至出售事项及先前出售事项完成后，标的股份及先前出售股份整体实现税前溢利约人民币33.61亿元。其中，集团预期于2020年度将取得税前溢利约人民币18.76亿元。\n\n于出售事项及先前出售事项完成后，集团通过聚金物业及润鼎物业将合共持有7.13亿股金科股份，约占金科地产已发行股本总数的13.35%。", "duration": {"day": 4, "hour": 0, "min": 2, "sec": 0}, "end_time": "2020-04-14T15:09:00", "id": 8, "location": "上海人民广场", "notice": "集团预期自投资金科股份起至出售事项及先前出售事项完成后，标的股份及先前出售股份整体实现税前溢利约人民币33.61亿元。其中，集团预期于2020年度将取得税前溢利约人民币18.76亿元。\n\n于出售事项及先前出售事项完成后，集团通过聚金物业及润鼎物业将合共持有7.13亿股金科股份，约占金科地产已发行股本总数的13.35%。", "others": "交通安全", "start_time": "2020-04-10T15:07:00", "tag": "分享,文娱,学习", "title": "集善助盲摄影作品展", "isLike": false, "likeNum": 20, "isInterested": true, "volunteers": 10, "vision_impaireds": 40, "registered": false}, 
      {"adminId": 0, "content": "一方面，是巨头通过明示或暗示的方式，借财报等各种契机说自己的营收有多好，数十亿、百亿之类的字眼开始经常出现；\n\n另一边，是市场份额在剧烈洗牌后逐步走向稳定。不久前，Canalys发布的2019年第四季度中国公共云服务市场报告显示，阿里、腾讯、百度分列市场份额前三甲，其中增速也基本遵循“排位靠前则增速更低”的规律，例如BAT“老三”百度智能云收入同比增速97.9%，在中国市场排名第一。", "duration": {"day": 4, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-04-02T14:12:00", "id": 4, "location": "北京王府井新燕莎金街购物广场", "notice": "一方面，是巨头通过明示或暗示的方式，借财报等各种契机说自己的营收有多好，数十亿、百亿之类的字眼开始经常出现；\n\n另一边，是市场份额在剧烈洗牌后逐步走向稳定。不久前，Canalys发布的2019年第四季度中国公共云服务市场报告显示，阿里、腾讯、百度分列市场份额前三甲，其中增速也基本遵循“排位靠前则增速更低”的规律，例如BAT“老三”百度智能云收入同比增速97.9%，在中国市场排名第一。", "others": "", "start_time": "2020-03-29T14:12:00", "tag": "保健,其它", "title": "全新大型公益互动体验“非视觉太极”活动月", "isLike": false, "likeNum": 0, "isInterested": false, "volunteers": 10, "vision_impaireds": 40, "registered": false}, 
      {"adminId": 0, "content": "武汉市5.78万名高三年级毕业生和中职、技工学校毕业年级学生重返校园，迎来“特殊时期”开学复课第一天。至此，31个省份和新疆生产建设兵团中小学部分学段均已开学，18个省份和新疆生产建设兵团高校已开学。各地大中小学在坚持做好常态化疫情防控中陆续迎来“开学季”。", "duration": {"day": 1, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-03-30T09:44:00", "id": 3, "location": "Beijing", "notice": "武汉市5.78万名高三年级毕业生和中职、技工学校毕业年级学生重返校园，迎来“特殊时期”开学复课第一天。至此，31个省份和新疆生产建设兵团中小学部分学段均已开学，18个省份和新疆生产建设兵团高校已开学。各地大中小学在坚持做好常态化疫情防控中陆续迎来“开学季”。", "others": "", "start_time": "2020-03-29T09:44:00", "tag": "分享,文娱", "title": "今天是阴天", "isLike": true, "likeNum": 15, "isInterested": false, "volunteers": 10, "vision_impaireds": 40, "registered": false}, 
      {"adminId": 0, "content": "春暖花开，一起出门放风筝。", "duration": {"day": 1, "hour": 0, "min": 0, "sec": 0}, "end_time": "2020-03-27T16:29:40", "id": 2, "location": "zhejiang", "notice": "春暖花开，一起出门放风筝。", "others": "", "start_time": "2020-03-26T16:29:40", "tag": "运动,文娱,保健", "title": "今天天气好", "isLike": true, "likeNum": 15, "isInterested": false, "volunteers": 10, "vision_impaireds": 40, "registered": false}
    ]
  },
  
  onLaunch: function () {
    // 登录
    // wx.login({
    //   success: res => {
    //     // 发送 res.code 到后台换取 openId, sessionKey, unionId
    //     const token = res.code;
    //     this.globalData.token = token;
    //     const that = this;

    //     wx.getSetting({
    //       success: res => {
    //         if (res.authSetting['scope.userInfo']) {
    //           // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
    //           wx.getUserInfo({
    //             lang: "zh_CN",
    //             success: res => {
    //               // 可以将 res 发送给后台解码出 unionId
    //               this.globalData.userInfo = res.userInfo;
    //               this.globalData.isAuthorized = true;
    //               console.log(this.globalData.isAuthorized)

    //               // 检查是否已注册
    //               getRegisterStatus(token, function(res){
    //                 if(!res.openid){
    //                   return;
    //                 }
    //                 console.log(res.isRegistered)
    //                 wx.setStorageSync('openid', res.openid);
    //                 wx.setStorageSync('isRegistered', !!res.isRegistered);
    //                 wx.setStorageSync('auditStatus', res.auditStatus || "pending");
    //                 that.globalData.isRegistered = !!res.isRegistered;
    //                 // this.globalData.userInfo = res.userInfo;
    //             });    
    
    //               // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
    //               // 所以此处加入 callback 以防止这种情况
    //               if (this.userInfoReadyCallback) {
    //                 this.userInfoReadyCallback(res)
    //               }
    //             }
    //           })
    //         }
    //       }
    //     });   
    //   }
    // });

    //
  }
})