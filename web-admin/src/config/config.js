let env = process.env.NODE_ENV;

let baseUrl = '';

if (env === 'development') {
  // baseUrl = 'http://47.103.133.134:3000/'
  baseUrl = 'https://admin.grimm.huaxiaoinfo.com/service/'
} else if (env === 'production') {
  // baseUrl = 'https://admin.grimm.huaxiaoinfo.com/service/'

  baseUrl = 'http://47.103.133.134:3000/'
}

export default baseUrl;