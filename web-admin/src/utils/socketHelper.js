import client from 'socket.io-client';
import url from '../config/config';

function getNewUsersSockect() {
    let newUsersSockect = client.connect( url );
    console.log( "connect......" );
    newUsersSockect.on('connect',function() {
        console.log( "connected......" );
    });

    return newUsersSockect;
}

export const socketHelper = {
    getNewUsersSockect 
}