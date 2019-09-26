import React from "react";
import { Ionicons } from '@expo/vector-icons';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { createDrawerNavigator, createStackNavigator,
         createAppContainer } from 'react-navigation';
import { DrawerActions } from 'react-navigation-drawer';
import BartenderDetail from '../views/BartenderDetail.js';
import BarSearch from '../views/BarSearch.js';
import BarDetail from '../views/BarDetail.js';
import Home from '../views/Home.js';


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  menuOpen: {
    marginLeft: 10,
    marginTop: 10
  },
  menuClose: {
    marginLeft: 14,
    marginTop: 10
  }
});

export const DrawerNavigator = createDrawerNavigator({
  Home: {
    screen: Home,
    navigationOptions: ({ navigation }) => ({
      title: 'Home',
      drawerLabel: 'Home',
      drawerIcon: () => (
        <Ionicons name="ios-home" size={100} />
      )
    })
  },
  Bartender: {
    screen: BarDetail,
    navigationOptions: ({ navigation }) => ({
      title: 'Bartender',
      drawerLabel: 'Bartender',
      drawerIcon: () => (
          <Ionicons name="ios-home" size={100} />
      )
    })

  }
});


export const StackNavigator = createStackNavigator({
  DrawerNavigator: {
    screen: DrawerNavigator,
    navigationOptions: ({ navigation }) => {
      const { state } = navigation;

      if(state.isDrawerOpen) {
        return {
          headerLeft: ({titleStyle}) => (
            <TouchableOpacity onPress={() => {navigation.dispatch(DrawerActions.toggleDrawer())}}>
              <Ionicons name="ios-close" style={styles.menuClose} size={36} color={titleStyle} />
            </TouchableOpacity>
          )
        };
      }
      else {
        return {
          headerLeft: ({titleStyle}) => (
            <TouchableOpacity onPress={() => {navigation.dispatch(DrawerActions.toggleDrawer())}}>
              <Ionicons name="ios-menu" style={styles.menuOpen} size={32} color={titleStyle} />
            </TouchableOpacity>
          )
        };
      }
    }
  }
});


export const MainNavigator = createStackNavigator({
  Home: {screen: Home},
  Bar: {screen: BarDetail},
  Bartender: {screen: BartenderDetail},
  BarSearch: {screen: BarSearch}
});
