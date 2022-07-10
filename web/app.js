const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");
const net = require('net');
const axios = require('axios');
const path = require('path');

const app = express();
const httpServer = createServer(app);
const port = 3000
const portList = [3001, 3002, 3003, 3004]
const modeList = ["none", "none", "none", "none"]
const dataList = Object()

portList.forEach((portNum) => {
    dataList[portNum] = []
});

const io = new Server(httpServer, {
    cors: {
        origin: "http://localhost:5000",
        methods: ["GET", "POST"]
    }
});

httpServer.listen(port, (socket) => {
    console.log(`app listening at http://localhost:${port}`)
})

io.on("connection", (socket) => {
    console.log(`connection on: ${socket.id}`)

    socket.on("join", async (data) => {
        socket.join(data)
    });

    socket.on('mode', async (packet) => {
        console.log(`mode change to ${packet.mode}`)
        modeList[packet.port - 3000] = packet.mode
    });
});

function makeSensorSocket(port) {
    const server = net.createServer((client) => {
        console.log('Client connection: ');
        console.log('   local = %s:%s', client.localAddress, client.localPort);
        console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);

        client.setTimeout(500);
        client.setEncoding('utf8');

        client.on('data', async (packet) => {
            const datas = packet.toString().split("\t")
            const last = datas.pop()

            dataList[port].push(...datas)

            const sockets = await io.in(port.toString()).fetchSockets();
            //sockets.forEach(async (socket) => {
            //    socket.emit("data", { date: ".", data: 12})
            //});

            // const maxDataSize = 5
            const maxDataSize = 50000
            if (dataList[port].length > maxDataSize) {
                if (modeList[port - 3000] != 'none') {
                    axios({
                        method: 'post',
                        url: `http://127.0.0.1:8000/model/${modeList[port - 3000]}`,
                        data: {
                            array: dataList[port],
                        }
                    }).then((response) => {
                        sockets.forEach(async (socket) => {
                            socket.emit("model_result", { res: response.data })
                        });
                    }).catch((error) => {
                        console.log("error")
                        console.log(error.message)
                        // console.log(error.request)
                        console.log("modeList")
                        console.log(modeList)
                    })
                }
                dataList[port] = []
            }
        });

        client.on('end', () => {
            console.log('Client disconnected');
        });

        client.on('error', (err) => {
            console.log('Socket Error: ', JSON.stringify(err));
        });

        client.on('timeout', () => {
            console.log('Socket Timed out');
        });
    });

    server.listen(port, () => {
        console.log('Server listening: ' + JSON.stringify(server.address()));
        server.on('close', () => {
            console.log('Server Terminated');
        });
        server.on('error', (err) => {
            console.log('Server Error: ', JSON.stringify(err));
        });
    });
}

portList.forEach((port) => {
    makeSensorSocket(port)
})

const webApp = express();
const webAppPort = 5000;

webApp.use(express.static('public'));
webApp.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'public', 'index.html'));
});
webApp.listen(webAppPort, () => {
    console.log(`web is open at \t http://localhost:${webAppPort}`);
});