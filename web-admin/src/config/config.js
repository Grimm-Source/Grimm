let env = process.env.NODE_ENV;

let baseUrl = '';

if (env === 'development') {
  baseUrl = 'http://173.37.22.10:18001/'
} else if (env === 'production') {
  baseUrl = 'http://47.103.133.134:18001/'
}

export default baseUrl;