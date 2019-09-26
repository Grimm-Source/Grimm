import { List, Skeleton } from 'antd';
import React from 'react';
import { hideDrawer, switchHomeTag, setNoticeUsers} from '../../actions';
import { HOME_TAG_TYPE } from "../../constants";
import { connect } from 'react-redux';

import './NoticeUserList.less';

class NoticeUserList extends React.Component {
  render() {
    return (
            <List
                className="new-user-list"
                loading={this.props.loading}
                itemLayout="horizontal"
                dataSource={this.props.newUsers}
                renderItem={item => (
                <List.Item className="item"
                    onClick={this.props.onClickNewUser.bind(this, item)}
                >
                    <Skeleton title={false} loading={this.props.loading} active>
                    <List.Item.Meta
                        title={<span><span className="user-name">{item.name}</span> | <span>{item.registerDate}</span></span>}
                    />
                    </Skeleton>
                </List.Item>
                )}
            />
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  // newUsers: state.notice.newUsers ,
  newUsers: [{
    id: 1,
    name: "张阿贵",
    registerDate: "2019-01-01"
  },{
    id: 2,
    name: "王小月",
    registerDate: "2019-09-21"
  }],
  loading: state.ui.loading
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickNewUser : (user) => {
    dispatch(hideDrawer());
    dispatch(switchHomeTag( HOME_TAG_TYPE.USER))
    dispatch(setNoticeUsers([]));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(NoticeUserList)