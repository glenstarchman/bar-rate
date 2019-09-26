import React from 'react';
import { Stylesheet, Text } from "react-native";

const styles = {
  link: {
    color: "#1B95E0"
  }
};


export const Link = props => (
  <Text
    {...props}
    accessibilityRole="link"
    style={styles.link}
  />
);
