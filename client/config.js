const __getUrl = function(){
  let version = __wxConfig.envVersion;

  switch (version)
  {
    case 'develop':
      return 'http://47.103.133.134:3000/';
    case 'trial':
      return 'http://47.103.133.134:3000/';
    case 'release':
      return 'http://47.103.133.134:3000/';
    default:
      return 'http://47.103.133.134:3000/';
  }
}

const config = {
  apiUrl: __getUrl()
};

module.exports = config;
