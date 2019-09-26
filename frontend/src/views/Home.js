import React from "react";
import { Button, Image, StyleSheet, Text, View } from "react-native";
import Base from './Base.js';
import {Link} from '../components/Link.js';
import * as taggable from '../services/taggable.service.js';

import {Like} from '../components/buttons/Like.js';


class Home extends Base {

  static navigationOptions = {
    title: 'Home',
  };


  componentDidMount() {
    this.setState({
      isLoading: false
    });
  }

  realRender() {
    return (
      <View style={styles.app}>
        <View style={styles.header}>
          <Text style={styles.title}>React Native for Web</Text>
        </View>
        <Text style={styles.text}>
          This is an example of an app built with{" "}
          <Link href="https://github.com/facebook/create-react-app">
            Create React App
          </Link>{" "}
          and{" "}
          <Link href="https://github.com/necolas/react-native-web">
            React Native for Web
          </Link>
        </Text>
        <Text style={styles.text}>
          To get started, edit{" "}
          <Link href="https://codesandbox.io/s/q4qymyp2l6/" style={styles.code}>
            src/App.js
          </Link>
          .
        </Text>
        <Button onPress={() => this.navigate('Bartender', {id: 1})} title="Bartender" />
        <Button onPress={() => this.navigate('Bar', {id: 1})} title="Bar" />
        <Button onPress={() => this.navigate('Profile', {id: 1})} title="Profile" />
        <Button onPress={() => this.navigate('BarSearch', {id: 1})} title="Searching Bars" />

        <Like objType={'bar'} objId={1}/>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  app: {
    marginHorizontal: "auto",
    maxWidth: 500
  },
  logo: {
    height: 80
  },
  header: {
    padding: 20
  },
  title: {
    fontWeight: "bold",
    fontSize: 16,
    marginVertical: "auto",
    textAlign: "center"
  },
  text: {
    lineHeight: 18,
    fontSize: 16,
    textAlign: "center"
  },
  link: {
    color: "#1B95E0"
  },
  code: {
    fontFamily: "monospace, monospace"
  }
});

export default Home;
