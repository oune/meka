const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");

const app = express();
const httpServer = createServer(app);
const httpServer2 = createServer(app);
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


var net = require('net');
var server0 = net.createServer(function (client) {
    console.log('Client connection: ');
    console.log('   local = %s:%s', client.localAddress, client.localPort);
    console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);

    client.setTimeout(500);
    client.setEncoding('utf8');

    client.on('data', function (packet) {
        console.log('server 0')
        console.log('Received data from client on port %d: %s', client.remotePort, packet.toString());
        console.log('  Bytes received: ' + client.bytesRead);
        const strs = packet.toString().split("\t")

        const date = strs[0]
        const data = strs[1]
        console.log(date)
        console.log(data)
        console.log('----------------------------------------')
    });

    client.on('end', function () {
        console.log('Client disconnected');
        server.getConnections(function (err, count) {
            console.log('Remaining Connections: ' + count);
        });
    });

    client.on('error', function (err) {
        console.log('Socket Error: ', JSON.stringify(err));
    });

    client.on('timeout', function () {
        console.log('Socket Timed out');
    });
});
server0.listen(3001, function () {
    console.log('Server listening: ' + JSON.stringify(server0.address()));
    server0.on('close', function () {
        console.log('Server Terminated');
    });
    server0.on('error', function (err) {
        console.log('Server Error: ', JSON.stringify(err));
    });
});

var net = require('net');
var server1 = net.createServer(function (client) {
    console.log('Client connection: ');
    console.log('   local = %s:%s', client.localAddress, client.localPort);
    console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);

    client.setTimeout(500);
    client.setEncoding('utf8');

    client.on('data', function (packet) {
        console.log('server 1')
        console.log('Received data from client on port %d: %s', client.remotePort, packet.toString());
        console.log('  Bytes received: ' + client.bytesRead);
        const strs = packet.toString().split("\t")

        const date = strs[0]
        const data = strs[1]
        console.log(date)
        console.log(data)
        console.log('----------------------------------------')
    });

    client.on('end', function () {
        console.log('Client disconnected');
        server.getConnections(function (err, count) {
            console.log('Remaining Connections: ' + count);
        });
    });

    client.on('error', function (err) {
        console.log('Socket Error: ', JSON.stringify(err));
    });

    client.on('timeout', function () {
        console.log('Socket Timed out');
    });
});
server1.listen(3002, function () {
    console.log('Server listening: ' + JSON.stringify(server1.address()));
    server1.on('close', function () {
        console.log('Server Terminated');
    });
    server1.on('error', function (err) {
        console.log('Server Error: ', JSON.stringify(err));
    });
});