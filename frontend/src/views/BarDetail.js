import React from 'react';
import BaseView from './Base.js';
import {getBar} from '../services/bar.service.js';
import { FlatList, ActivityIndicator, Text, View  } from 'react-native';

export default class Bar extends BaseView {


  componentDidMount() {
    const id = this.navigation.getParam('id', 'NO-ID');
    return getBar(id)
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          dataSource: [responseJson.data]
        });
        this.changeTitle(responseJson.data.name);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  realRender() {
    const data = this.state.dataSource[0];
    return (
        <View style={{flex: 1 , paddingTop:20}}>
          <Text>This is info for {data.name}</Text>
        </View>
    );
  }
}
