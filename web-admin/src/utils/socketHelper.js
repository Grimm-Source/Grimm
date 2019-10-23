import client from 'socket.io-client';
import url from '../config/config';
import { storage } from '../utils/localStorageHelper';

const NEW_USERS = 'new-users';

let user = storage.getItem("user");

function getNewUsersSockect() {
    let newUsersSockect = client.connect( url + NEW_USERS );

    newUsersSockect.on('connect',function() {
        newUsersSockect.emit("connect", { data: {
            user: user.id
        }});
    });

    return newUsersSockect;
}

export const socketHelper = {
    getNewUsersSockect 
}