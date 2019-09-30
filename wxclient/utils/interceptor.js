const apiUrl = require('../config.js').apiUrl;

const request = (option, isManualLoading = false) => {
    if(!option.url){
        return;
    }

    if(!isManualLoading){
        wx.showLoading();
    }
    
    return new Promise((resolve, reject) => {

        let obj = {
            url: `${apiUrl}${option.url}`,
            header: {
                'Content-type': 'application/json',
                'Authorization': wx.getStorageSync('openid'),
            },
            method: option.method || "GET",
            success: (res) =>{
                if(res.statusCode >= 400){
                    reject('网络失败，请稍后再试');
                }else{
                    if(res.data.error){
                        reject(res.data.error);
                    }else{
                        if(res.data.status === "failure" ){
                            reject(res.data.message);
                            return;
                        }else if(res.data.status === "success"){
                            resolve();
                            return;
                        }
                        resolve(res.data);
                    }
                }
            },
            error: () => {
                reject('网络失败，请稍后再试');
            },
            complete: ()=>{
                if(isManualLoading){
                    return;
                }
                wx.hideLoading();
            }
        }
        if(option.method === "POST"){
            obj["data"] = option.data;
        }
        
        wx.request(obj);

     }).then((data)=>{
        option.success && option.success(data);
     },(error)=>{
        option.fail && option.fail(error);
     })
}

module.exports = {
    request
}
  