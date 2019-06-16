import React from 'react';
import { Button, Stylesheet, Text } from "react-native";
import {addLike} from '../services/taggable.service.js';


export const Like = (props) => (
    <Button
      accessibilityRole="link"
      style={styles.link}
      {...props}
      onClick={() => addLike(props.objType, props.objId)}
    />
);

const styles = {
  link: {
    color: "#1B95E0"
  }
};
