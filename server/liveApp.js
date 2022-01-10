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
    console.log(`connection on: ${socket.id}`)
    sockets.push(socket)
});

const sockets = []
httpServer.listen(port, (socket) => {
    console.log(`Example app listening at http://localhost:${port}`)
})

setInterval(() => {
    // console.log("!")
    sockets.forEach((socket) => {
        socket.emit("data", Math.random() * 20)
    })
}, 1000)