Page({
  data: {
    activity_id: '',
    title: '',
    date: '',
    address: '',
  },
  onLoad: function (option) {
    this.setData({
      activity_id: option.activity_id,
      title: option.title,
      date: option.date,
      address: option.address,
    });
  },

  onTapWillingPickup: function () {
    let url = '../pickupVolunteer/pickupVolunteer?activity_id=' + this.data.activity_id + '&'
    url = url + 'title=' + this.data.title + '&'
    url = url + 'date=' + this.data.date + '&'
    url = url + 'address=' + this.data.address + '&'
    wx.navigateTo({
      url: url
    });
  },

  onTapConsiderPickup: function () {
    wx.navigateBack({
      delta: 1,
    })
  },

  onTapUnwillingPickup: function () {
    wx.navigateBack({
      delta: 1,
    })
  },
})