import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import initialState from './utils/initialStateHelper';
// import * as serviceWorker from './serviceWorker';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import { ConfigProvider } from 'antd';
import zh_CN from 'antd/lib/locale-provider/zh_CN';
import moment from 'moment';
import 'moment/locale/zh-cn';
import thunk from 'redux-thunk';
import reducer from './reducers';


const middleware = [ thunk ];
moment.locale('zh-cn');

const store = createStore(reducer, initialState, applyMiddleware(...middleware));
ReactDOM.render(<Provider store={store}>
    <ConfigProvider locale={zh_CN}><App/></ConfigProvider>
  </Provider>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
