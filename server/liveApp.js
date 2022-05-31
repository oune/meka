const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");
const net = require('net');
const axios = require('axios');

const app = express();
const httpServer = createServer(app);
const port = 3000
const portList = [3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008]
const dataList = Object()

portList.forEach((portNum) => {
    dataList[portNum] = []
});

console.log(dataList)

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
        await console.log(`connection on: ${socket.id}`)
        await console.log(`data : ${data}`)

        socket.join(data)
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
            const strs = packet.toString().split("\t")
            const date = strs[0]
            const data = strs[1]

            dataList[port].push(data)

            const sockets = await io.in(port.toString()).fetchSockets();
            sockets.forEach(async (socket) => {
                socket.emit("data", { date: date, data: data })
            });

            const maxDataSize = 4
            if (dataList[port].length > maxDataSize) {
                axios({
                    method: 'post',
                    url: 'http://127.0.0.1:8000/model/pump',
                    data: {
                        array: dataList[port],
                    }
                }).then((response) => {
                    console.log(response.data)
                    sockets.forEach(async (socket) => {
                        socket.emit("model_result", { res: response.data })
                    });
                })
                dataList[port] = []
            }
        });

        function log() {
            console.log(dataList)
            console.log(`server ${port}`)
            console.log('Received data from client on port %d: %s', client.remotePort, packet.toString());
            console.log('  Bytes received: ' + client.bytesRead);
            console.log(date)
            console.log(data)
            console.log('----------------------------------------')
        }

        client.on('end', () => {
            console.log('Client disconnected');
            server.getConnections((err, count) => {
                console.log('Remaining Connections: ' + count);
            });
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