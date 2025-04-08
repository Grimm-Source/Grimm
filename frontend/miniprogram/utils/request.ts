// utils/request.js
const request = (
  url,
  method = 'GET',
  data = {},
  header = {
    'content-type': 'application/json',
    'Authorization': wx.getStorageSync('openid')
  }
) => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `https://wxapi.rp-i.net/${url}`,
      method: method,
      data: data,
      header: header,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(`Server Error: ${res.statusCode}`)
        }
      },
      fail: (err) => {
        reject(`Network Error: ${err}`)
      }
    })
  })
}

module.exports = {
  request
};