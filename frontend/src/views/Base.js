import React from 'react';
import {callApi} from '../api/fetcher.js';
import { ActivityIndicator, View  } from 'react-native';


export default class BaseView extends React.Component {

  static navigationOptions = ({ navigation }) => {
    try {
      const {state} = navigation;
      return {
        title: `${state.params.title}`,
      };
    } catch {
    }
  };

  changeTitle(text) {
    const {setParams} = this.props.navigation;
    setParams({ title: text });
  }

  constructor(props) {
    super(props);
    this.state = { isLoading: true };
    const { navigation } = this.props;
    this.navigation = navigation;
  }


  navigate(view, data) {
    this.navigation.navigate(view, data);
  }

  render() {

    if(this.state.isLoading) {
      return(
          <View style={{flex: 1, padding: 20}}>
          <ActivityIndicator/>
          </View>
      );
    }

    return this.realRender();
  }
}
