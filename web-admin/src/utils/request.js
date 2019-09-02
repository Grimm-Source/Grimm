import url from '../config/config'

const request = (options) => {
    if(options.method === "POST"){
        return fetch(`${url}${options.path}`,{
            method: 'POST',
            headers: {
                Accept: 'application/json',
            },
            body: JSON.stringify(options.data)
        }).then(response => {
            if(response.status >= 400 && response.status < 500){
                return Promise.reject("请联系管理员");
            }else if(response.status >= 500 ){
                return Promise.reject("网络问题，请稍后重试");
            }
            return response.json()});
    }

    return fetch(`${url}${options.path}`,{
        method: 'GET',
        headers: {
            Accept: 'application/json',
        }
    }).then(response => {
        if(response.status >= 400){
            if(response.status >= 400 && response.status < 500){
                return Promise.reject("请联系管理员");
            }else if(response.status >= 500 ){
                return Promise.reject("网络问题，请稍后重试");
            }
        }
        return response.clone().json()}
    )
}

export default request;