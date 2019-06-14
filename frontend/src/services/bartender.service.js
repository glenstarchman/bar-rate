import {callApi} from '../common/fetcher.js';



export const getBartender = (id) => {
  let url = `bartender/${id.toString()}/`;
  return callApi(url, 'GET', null);
}
