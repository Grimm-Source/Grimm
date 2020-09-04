const __getUrl = function(){
  let version = __wxConfig.envVersion;

  switch (version)
  {
    case 'develop':
      return 'https://admin.grimm.huaxiaoinfo.com/service/';
    case 'trial':
      return 'https://admin.grimm.huaxiaoinfo.com/service/';
    case 'release':
      return 'https://admin.grimm.huaxiaoinfo.com/service/';
    default:
      return 'https://admin.grimm.huaxiaoinfo.com/service/';
  }
}

const config = {
  apiUrl: __getUrl()
};

module.exports = config;
