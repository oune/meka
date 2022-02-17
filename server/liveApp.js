const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");
const net = require('net');

const app = express();
const httpServer = createServer(app);
const port = 3000

const io = require("socket.io")(httpServer, {
    cors: {
        origin: "http://localhost:5000",
        methods: ["GET", "POST"]
    }
});

io.on("connection", (socket) => {
    sockets.push(socket)
    //log
    console.log(`connection on: ${socket.id}`)
    console.log(`total sockets: ${sockets.length}`)
});

const sockets = []
httpServer.listen(port, (socket) => {
    console.log(`Example app listening at http://localhost:${port}`)
})

setInterval(() => {
    sockets.forEach((socket) => {
        const vide = Math.random() * 2
        const temp = Math.random() * 30
        socket.emit("data", { vibe: vide, temp: temp })
    })
}, 1000)

function makeSensorSocket(port) {
    const server = net.createServer((client) => {
        console.log('Client connection: ');
        console.log('   local = %s:%s', client.localAddress, client.localPort);
        console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);

        client.setTimeout(500);
        client.setEncoding('utf8');

        client.on('data', (packet) => {
            console.log(`server ${port}`)
            console.log('Received data from client on port %d: %s', client.remotePort, packet.toString());
            console.log('  Bytes received: ' + client.bytesRead);
            const strs = packet.toString().split("\t")

            const date = strs[0]
            const data = strs[1]
            console.log(date)
            console.log(data)
            console.log('----------------------------------------')
        });

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

const portList = [3001, 3002]
portList.forEach((port) => {
    makeSensorSocket(port)
})