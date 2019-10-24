import client from 'socket.io-client';
import url from '../config/config';
import { storage } from '../utils/localStorageHelper';

let user = storage.getItem("user");

function getNewUsersSockect() {
    let newUsersSockect = client.connect( url );
    console.log( "connect......" );
    newUsersSockect.on('connect',function() {
        console.log( "connected......" );
        newUsersSockect.emit("test", { data: {
            user: user.id
        }});
    });

    return newUsersSockect;
}

export const socketHelper = {
    getNewUsersSockect 
}