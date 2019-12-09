import { List, Skeleton } from 'antd';
import React, { Fragment } from 'react';
import { hideDrawer, switchHomeTag, setNoticeUsers} from '../../actions';
import { HOME_TAG_TYPE } from "../../constants";
import { connect } from 'react-redux';
import { withRouter} from "react-router-dom";
import './NoticeUserList.less';

const MAX_ITEMS = 10;

class NoticeUserList extends React.Component {

  onClickNewUser(item){
    this.props.history.push('/users');
    this.props.onClickNewUser(item);
  }

  render() {
    let isShowMore = this.props.newUsers.length > MAX_ITEMS;
    let listedUsers =  isShowMore? this.props.newUsers.slice(0, 11): this.props.newUsers;
    return (
      <Fragment>
            <List
                className="new-user-list"
                loading={this.props.loading}
                itemLayout="horizontal"
                dataSource={listedUsers}
                renderItem={item => (
                <List.Item className="item"
                    onClick={this.onClickNewUser.bind(this, item)}
                >
                    <Skeleton title={false} loading={this.props.loading} active>
                    <List.Item.Meta
                        title={<span><span className="user-name">{item.name}</span> | <span>{item.registrationDate}</span></span>}
                    />
                    </Skeleton>
                </List.Item>
                )}
            />
            {isShowMore?<span className="button" onClick={this.onClickNewUser} >更多...</span>: null}
      </Fragment>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  newUsers: state.notice.newUsers,
  loading: state.ui.loading
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickNewUser : (user) => {
    dispatch(hideDrawer());
    dispatch(switchHomeTag( HOME_TAG_TYPE.USER))
    dispatch(setNoticeUsers([]));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(NoticeUserList))