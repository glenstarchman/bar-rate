import {callApi} from '../common/fetcher.js';

export const getBar = (id) => {
  let url = `bar/${id.toString()}/`;
  return callApi(url, 'GET', null);
};


export const searchBar = (params) => {
  let url = "bar/";
  return callApi(url, 'GET', params);
};
