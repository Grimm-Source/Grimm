import React from 'react';
import { Button } from 'antd';
import { connect } from 'react-redux';
import refresh from '../../images/refresh.svg';
import TableHeader from '../../components/TableHeader/TableHeader';
import UserTable from '../../components/UserTable/UserTable';

import './User.less';

class User extends React.Component {  
  render() {
    return (
        <div className="user">
            <TableHeader right={<span>
                      <Button >同意</Button>
                      <Button type="danger">拒绝</Button>
                      <img 
                        width={25}
                        alt="refresh"
                        src={refresh}
                      />
                      </span>}/>
            <UserTable/>
        </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading
});

export default connect(mapStateToProps)(User)