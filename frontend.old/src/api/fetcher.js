/* API helper */
import {API_ROOT} from '../config.js';

export function authHeader() {
  // return authorization header with rest-framework token
  let user = JSON.parse(localStorage.getItem('user'));

  if (user && user.auth_token && user.auth_token.key) {
    return {'Authorization': 'Token ' +   user.auth_token.key};
  } else {
    return {};
  }
}

export function callApi(endpoint, method, data) {

  let url = API_ROOT +  "/" + endpoint;

  let headers = authHeader();
  headers['Content-Type'] = 'application/json';
  let options = {
    method: method,
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin', // include, *same-origin, omit
    headers: headers,
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // no-referrer, *client
  };

  if (method != 'HEAD' && method != 'GET' && data) {
    options['body'] = JSON.stringify(data);
  }

  return fetch(url, options)
    .then(response => response.json())
    .catch((error) => console.log(error));
}
