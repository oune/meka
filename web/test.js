const axios = require('axios');

axios({
    method: 'post',
    url: `http://202.31.197.145:21/model/pump`,
    data: {
        array: [1, 2, 3, 4],
    }
}).then((response) => {
    console.log(response.data);
}).catch((error) => {
    console.log("error")
    console.log(error.message)
    console.log(error.request)
})