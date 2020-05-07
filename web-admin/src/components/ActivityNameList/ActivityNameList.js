import React from 'react';
import { Table, Input, Button, Icon } from 'antd';
import Highlighter from 'react-highlight-words';
import { getActivityNameList } from '../../actions';
import { connect } from 'react-redux';

import './ActivityNameList.less';

class ActivityNameList extends React.Component {

      constructor(props){
        super(props);
        this.state = {
          searchText: '',
          sortedInfo: null
        };
      }

      componentDidMount(){
        this.props.getActivityNameList(this.props.activityId);
      }

      onClickDownload=()=>{
        if(this.props.loading){
          return;
        }
        const header = "\ufeff"+"序号,活动名称,姓名,类型,是否接送,对接人,状态\n";
        const rows = [];
        this.props.activityNameList.forEach(function(item) {
              rows.push(item.id + ',' + item.activity + ',' + item.name + ',' 
              + (item.type==="volunteer"?"志愿者":"视障人士") + ',' + (item.pickUp?"是":"否") +',' 
              + (item.pickUpName?item.pickUpName:"") + ',' + item.status);
            })
        const csvString = header + rows.join('\n');
        const link = window.document.createElement('a');
        document.body.appendChild(link);
        link.href = window.URL.createObjectURL(new Blob([csvString], { type: "text/plain;charset=utf-8" }));
        link.download = '活动名单.csv';
        link.click();
        document.body.removeChild(link);
    }
    
      getColumnSearchProps = (dataIndex, title) => ({
        filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
          <div style={{ padding: 8 }}>
            <Input
              ref={node => {
                this.searchInput = node;
              }}
              placeholder={`搜索${title}`}
              value={selectedKeys[0]}
              onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
              onPressEnter={() => this.handleSearch(selectedKeys, confirm)}
              style={{ width: 188, marginBottom: 8, display: 'block' }}
            />
            <Button
              type="primary"
              onClick={() => this.handleSearch(selectedKeys, confirm)}
              icon="search"
              size="small"
              style={{ width: 90, marginRight: 8 }}
            >
              搜索
            </Button>
            <Button onClick={() => this.handleReset(clearFilters)} size="small" style={{ width: 90 }}>
              重置
            </Button>
          </div>
        ),
        filterIcon: filtered => (
          <Icon type="search" style={{ color: filtered ? '#1890ff' : undefined }} />
        ),
        onFilter: (value, record) =>
          record[dataIndex]
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: visible => {
          if (visible) {
            setTimeout(() => this.searchInput.select());
          }
        },
        render: text => (
          <Highlighter
            highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
            searchWords={[this.state.searchText]}
            autoEscape
            textToHighlight={text?text.toString():''}
          />
        ),
      });
    
      handleSearch = (selectedKeys, confirm) => {
        confirm();
        this.setState({ searchText: selectedKeys[0] });
      };
    
      handleReset = clearFilters => {
        clearFilters();
        this.setState({ searchText: '' });
      };
    
      handleChange = (sorter) => {
        this.setState({
          sortedInfo: sorter
        });
      };
    
      render() { 
        let { sortedInfo } = this.state;
        sortedInfo = sortedInfo || {}; 
        const columns = [
          {
            title: '序号',
            dataIndex: 'id',
            width: '10%',
            sorter: (a, b) => a.id - b.id,
          },
          {
            title: '用户',
            dataIndex: 'name',
            width: '25%',
            ...this.getColumnSearchProps('name', '用户'),
          },
          {
            title: '类型',
            dataIndex: 'type',
            width: '10%',
            sorter: (a, b) => a.type.localeCompare(b.type),
            render:(type)=>(
              type === "volunteer"?"志愿者":"视障人士"
            )
          },
          {
            title: '是否接送',
            dataIndex: 'pickUp',
            width: '10%',
            sorter: (a, b) => a.pickUp - b.pickUp,
            render:(pickUp)=>(
              pickUp?"是":"否"
            )
          },
          {
            title: '对接人',
            dataIndex: 'pickUpName',
            width: '25%',
            ...this.getColumnSearchProps('pickUpName', '对接人'),
          },
          {
            title: '状态',
            dataIndex: 'status',
            width: '15%',
            sorter: (a, b) => b.status.localeCompare(a.status),
          }
        ];
        if(!this.props.activityId){
            columns.splice(1,0,{
                title: '活动',
                dataIndex: 'activity',
                key: 'activity',
                width: '15%',
                ...this.getColumnSearchProps('activity', '活动'),
              });
        }
        return <div className="activity-name-list">
                <Table rowKey="id" loading={this.props.loading} size="small" columns={columns} dataSource={this.props.activityNameList} 
                  onChange={this.handleChange} footer={() => <Button type="link" onClick={this.onClickDownload}>下载名单</Button>}
                  pagination={{  
                    pageSize: this.props.activityId? 10:20,
                    showTotal: (total, range) => this.props.activityId?<span>{`${range[0]}-${range[1]}项，共${total}项`}</span>:<span style={{color:"white"}}>{`${range[0]}-${range[1]}项，共${total}项`}</span>
                  }}/>
                </div>;
      }
}

const mapStateToProps = (state, ownProps) => ({
    loading: state.ui.loading,
    activityId: state.ui.activityId,
    activityNameList: state.ui.activityNameList
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  getActivityNameList : (activityId) => {
    dispatch(getActivityNameList(activityId));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(ActivityNameList)