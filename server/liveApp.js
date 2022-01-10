const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");

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