import React, {useState, useEffect, useLayoutEffect, useRef} from 'react';
import { Button, Stylesheet, Text } from "react-native";
import * as taggable from '../../services/taggable.service.js';

/* a button  that toggles liking of a taggable object */

const styles = {
  link: {
    color: "#1B95E0"
  }
};

export function Like (props) {

  const [toggle, setToggle] = useState(false);
  const [likeId, setLikeId] = useState(null);
  const [initial, setInitial] = useState(true);
  const [loading, setLoading] = useState(true);
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {

    function getLike() {
      return taggable.doesUserLike(props.objType, props.objId)
                     .then((results) => {
                       setToggle(results.data.likes);
                       setLikeId(results.data.taggable_id);
                       firstUpdate.current = false;
                     });
    }

    if (firstUpdate.current) {
      //first load so get the like
      getLike();
      return;
    }

    console.log(`toggle=${toggle}`)
    if (toggle)  {
      firstUpdate.current = false;
      taggable.addLike(props.objType, props.objId)
        .then((result) => {
          setLikeId(result.data.taggable_id);
        })
    } else if (!toggle) {
      firstUpdate.current = false;
      //deleting a like
      if (likeId != null) {
        console.log('deleting');
        taggable.deleteLike(props.objType, props.objId, likeId);
        setLikeId(null);
      }
    }
  }, [toggle]);

  return (
    <Button
      accessibilityRole="link"
      style={styles.link}
      {...props}
      onPress={() => setToggle(!toggle)}
      title={likeId ? likeId : 'not liked'}
    />
  );

};
