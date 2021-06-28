const __getUrl = function(){
  let version = __wxConfig.envVersion;

  switch (version)
  {
    case 'develop':
      // return 'https://wxapi.rp-i.net/';
      return 'http://10.140.208.17:5000';
    case 'trial':
      return 'https://wxapi.rp-i.net/';
    case 'release':
      return 'https://wxapi.rp-i.net/';
    default:
      return 'https://wxapi.rp-i.net/';
  }
}

const config = {
  apiUrl: __getUrl()
};

module.exports = config;
