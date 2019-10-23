function clearItems() {
    sessionStorage.clear();
}

function setItem(key, value) {
    sessionStorage.setItem(key + "", JSON.stringify(value));
}

function setItems(obj) {
    let keys = Object.keys(obj);
    keys.forEach((key)=>{
        sessionStorage.setItem(key + "",  JSON.stringify(obj[key]));
    });
}

function getItem(key) {
    return JSON.parse(sessionStorage.getItem(key));
}

export const storage = {
    getItem,
    setItem,
    setItems,
    clearItems
}


