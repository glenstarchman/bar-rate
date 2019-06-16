import {callApi} from '../common/fetcher.js';

//generic functions for handing taggable info


export const addTaggable = (objType, objId, taggableType, payload) => {
  let url = `${objType}/${objId}/${taggableType}/`;
  return callApi(url, 'POST', payload);
};

export const getTaggable = (objType, objId, taggableType) => {
  let url = `${objType}/${objId}/${taggableType}/`;
  return callApi(url, 'GET', null);
};

export const deleteTaggable = (objType, objId, taggableType, taggableId) => {
  let url = `${objType}/${objId}/${taggableType}/${taggableId}`;
  return callApi(url, 'DELETE', null);
}

export const getLikes = (objType, objId) => {
  return getTaggable(objType, objId, 'likes');
};

export const getDislikes = (objType, objId) => {
  return getTaggable(objType, objId, 'dislikes');
};

export const getComments = (objType, objId) => {
  return getTaggable(objType, objId, 'comments');
};

export const getReviews = (objType, objId) => {
  return getTaggable(objType, objId, 'reviews');
};

export const getImages = (objType, objId) => {
  return getTaggable(objType, objId, 'images');
};


export const addLike = (objType, objId) => {
  return addTaggable(objType, objId, 'like', null);
};

export const addDislike = (objType, objId) => {
  return addTaggable(objType, objId, 'dislike', null);
};

export const addComment = (objType, objId, payload) => {
  return addTaggable(objType, objId, 'comment', payload);
};

export const addReview = (objType, objId, payload) => {
  return addTaggable(objType, objId, 'review', payload);
};

export const addImage = (objType, objId, payload) => {
  return addTaggable(objType, objId, 'image', payload);
};

export const deleteLike = (objType, objId, taggableId) => {
  return deleteTaggable(objType, objId, 'like', taggableId);
}

export const deleteComment = (objType, objId, taggableId) => {
  return deleteTaggable(objType, objId, 'comment', taggableId);
}

export const deleteReview = (objType, objId, taggableId) => {
  return deleteTaggable(objType, objId, 'review', taggableId);
}

export const deleteImage = (objType, objId, taggableId) => {
  return deleteTaggable(objType, objId, 'image', taggableId);
}
