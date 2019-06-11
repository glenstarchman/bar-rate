import React from 'react';
import BaseView from './Base.js';
import {callApi} from '../common/fetcher.js';
import { FlatList, ActivityIndicator, Text, View  } from 'react-native';

export default class Bar extends BaseView {


  componentDidMount() {
    const id = this.navigation.getParam('id', 'NO-ID');
    let url = 'bar/' + id.toString();
    return callApi(url, 'GET', null)
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
    console.log(data);
    return (
        <View style={{flex: 1 , paddingTop:20}}>
          <Text>This is info for {data.name}</Text>
        </View>
    );
  }
}
