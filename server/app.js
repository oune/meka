const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
    res.send('main page')
})

app.get('/sensor/:sensorId', (req, res) => {
    const id = req.params.sensorId
    res.send(id)
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})