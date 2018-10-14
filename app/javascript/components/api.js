const axios = require('axios');

axios.defaults.baseURL = '/api/v1';

export default {
  getOfferings: async () => {
    return (await axios.get('offerings')).data
  }
}
