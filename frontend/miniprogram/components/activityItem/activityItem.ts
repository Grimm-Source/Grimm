// components/activityItem/activityItem.ts
import { apiUrl, formatDateTime } from '../../utils/util'

Component({

  /**
   * 组件的属性列表
   */
  properties: {
    activity: {
      type: Object,
      value: {}
    }
  },

  lifetimes: {
    attached() {
      this.formatter(this.data.activity);
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    id: '',
    title: '',
    banner: '',
    start_time: '',
    end_time: '',
    location: '',
    fee: '',
    registered: 0,
    interested: 0,
    thumbs_up: 0,
    share: 0
  },

  /**
   * 组件的方法列表
   */
  methods: {
    formatter(activity) {
      this.setData({
        id: activity.id,
        title: activity.title,
        banner: `${apiUrl}activity/themePic?activity_them_pic_name=${activity.activity_them_pic_name}`,
        start_time: formatDateTime(activity.start_time),
        end_time: formatDateTime(activity.end_time),
        location: activity.location,
        fee: activity.activity_fee > 0 ? `¥${activity.activity_fee}元` : '免费',
        registered: activity.registered,
        interested: activity.interested,
        thumbs_up: activity.thumbs_up,
        share: activity.share
      })
    },

    onRedirectToPageTap(event) {
      const activityId = event.currentTarget.dataset.activityId;
      wx.navigateTo({
        url:  `/pages/activityDetail/activityDetail?id=${activityId}`
      })
    }
  }
})