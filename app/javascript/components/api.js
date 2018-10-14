const axios = require('axios');
require('babel-polyfill')
axios.defaults.baseURL = '/api';

export default {
  getOfferings: async () => {
    return  axios.get('offerings')
  }
}
