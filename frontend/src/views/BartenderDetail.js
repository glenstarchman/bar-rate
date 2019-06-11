import React from 'react';
import BaseView from './Base.js';
import {callApi} from '../api/fetcher.js';
import { FlatList, ActivityIndicator, Text, View  } from 'react-native';

export default class BartenderDetail extends BaseView {


  componentDidMount() {
    const id = this.navigation.getParam('id', 'NO-ID');
    let url = 'bartender/' + id.toString();
    return callApi(url, 'GET', null)
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          dataSource: [responseJson.data]
        });
        this.changeTitle("Profile for " + responseJson.data.nickname);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  realRender() {
    return (
        <View style={{flex: 1 , paddingTop:20}}>
        <FlatList
          data={this.state.dataSource}
          renderItem={({item}) => <Text>{item.name}, {item.nickname}</Text>}
          keyExtractor={({id}, index) => id}
        />
        </View>
    );
  }
}
