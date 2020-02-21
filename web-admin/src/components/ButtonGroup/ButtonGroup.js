import { Button } from 'antd';
import React from 'react';

import './ButtonGroup.less';

const ADButtonGroup = Button.Group;

export default class ButtonGroup extends React.Component {
  constructor(props){
      super(props);
      let value = this.props.value || [];
      let map = {};
      value.forEach((item)=>{
        map[item]= true;
      });

      this.state={
        buttons: this.props.buttons || [],
        value,
        map
      }
  }

  onClickButton=(key)=>{
    let map = this.state.map;
    map[key] = !map[key];
    let result = [];
    for(let key in map){
        if(map[key]){
            result.push(key);
        }
    }
    this.setState({
        map
    });
    this.props.onChange(result);
  }

  getButtons=()=>{
    return this.props.buttons.map((item)=>{
        return <Button key={item} className={this.state.map[item]?'active-button':'inactive-button'} onClick={this.onClickButton.bind(this, item)}>{item}</Button>  
    })
  }

  render() {
    const buttons = this.getButtons();
    return (
        <ADButtonGroup className="button-group">
            {buttons}
        </ADButtonGroup>
    );
  }
}