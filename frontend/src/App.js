import React, { Component } from "react";

import {createAppContainer} from 'react-navigation';
import { DrawerNavigator, StackNavigator, MainNavigator } from './components/Navigation.js';

const App = createAppContainer(MainNavigator);

export default App;
