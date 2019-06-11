import {callApi} from '../common/fetcher.js';



export const getBar = (id) => {
  let url = 'bar/' + id.toString();
  return callApi(url, 'GET', null);
}
