import React, { Component } from "react";
import { Button, Image, StyleSheet, Text, View } from "react-native";
import BartenderDetail from './views/BartenderDetail.js';
import BarDetail from './views/BarDetail.js';
import Home from './views/Home.js';
import {Link} from './components/Link.js';

import {createAppContainer} from 'react-navigation';
import { DrawerNavigator, StackNavigator, MainNavigator } from './components/Navigation.js';

const App = createAppContainer(MainNavigator);

export default App;
