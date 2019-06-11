import React from 'react';
import {callApi} from '../api/fetcher.js';
import { FlatList, ActivityIndicator, Text, View  } from 'react-native';

export default class BartenderDetail extends React.Component {


  constructor(props){
    super(props);
    this.state = { isLoading: true };
  }

  componentDidMount() {
    let url = 'bartender/' + this.props.id.toString();
    return callApi(url, 'GET', null)
      .then((responseJson) => {
        console.log(responseJson);
        this.setState({
          isLoading: false,
          dataSource: [responseJson.data]
        });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {

    if(this.state.isLoading){
      return(
          <View style={{flex: 1, padding: 20}}>
          <ActivityIndicator/>
          </View>
      );
    }

    return(
        <View style={{flex: 1, paddingTop:20}}>
        <FlatList
          data={this.state.dataSource}
          renderItem={({item}) => <Text>{item.name}, {item.nickname}</Text>}
          keyExtractor={({id}, index) => id}
        />
        </View>
    );
  }
}
