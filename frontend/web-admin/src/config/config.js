let env = process.env.NODE_ENV;

let baseUrl = '';

if (env === 'development') {
  // baseUrl = 'http://10.79.99.193:5000/'
  baseUrl = "https://wxapi.rp-i.net/"
} else if (env === 'production') {
  baseUrl = "https://wxapi.rp-i.net/"

  // baseUrl = 'http://47.103.133.134:3000/'
}

export default baseUrl;