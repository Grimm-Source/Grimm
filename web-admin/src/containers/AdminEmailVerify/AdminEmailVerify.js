import React from 'react';
import {
    Modal,
    Result,
    Button
} from 'antd';
import {
    verifyAdminEmail,
    hideEmailVerify
} from '../../actions';
import {
    storage
} from '../../utils/localStorageHelper';
import {
    connect
} from 'react-redux';

import "./AdminEmailVerify.less";

class AdminEmailVerify extends React.Component {
    startButtonTimer = (timeInterval, buttonDiv) => {
        buttonDiv.setAttribute('timevalue', timeInterval);
        buttonDiv.setAttribute('clickable', 'false');
        var set = setInterval(function () {
            timeInterval--;
            buttonDiv.setAttribute('timevalue', timeInterval);
            if (timeInterval === 0) {
                buttonDiv.setAttribute('timevalue', '');
                buttonDiv.setAttribute('clickable', 'true');
                clearInterval(set);
            }
        }, 1000);
    }

    fetchEmailVerify = e => {
        e.preventDefault();
        let buttonDiv = e.target;
        if (!buttonDiv) return;
        let clickable = buttonDiv.getAttribute('clickable') === 'true';
        if (clickable) {
            this.props.verifyAdminEmail(this.props.emailAddr);
            this.startButtonTimer(60, buttonDiv); //set the time interval 60s.
        }
    }

    handleCancel = e => {
        e.preventDefault();
        this.props.hideEmailVerify();
    }

    render() {
        return ( <Modal className = "admin-email-verify" title = "邮箱验证"
            visible = { this.props.visible  }
            destroyOnClose = { true }
            closable = { true }
            maskClosable = { true }
            footer = { null }
            onCancel = { this.handleCancel } >
            <Result title = "您的邮箱还未验证！"
            status = "warning"
            extra = {
                <Button className = "admin-email-verify-button" type = "link" timevalue = "60" key = "console" clickable = "true"
                onClick = { this.fetchEmailVerify }> 点击验证邮箱 </Button>
            } /> 
            </Modal>
        );
    }
}

const mapStateToProps = (state, ownProps) => ({
    visible: state.ui.isShowEmailVerify,
    emailAddr: state.ui.emailAddrWaitForVerified
});

const mapDispatchToProps = (dispatch, ownProps) => ({
    verifyAdminEmail: (emailAddr) => {
        dispatch(verifyAdminEmail(emailAddr));
    },
    hideEmailVerify: () => {
        dispatch(hideEmailVerify());
    }
});

export default connect(mapStateToProps, mapDispatchToProps)(AdminEmailVerify)