import socketio

# standard Python
sio = socketio.Client()
sio.connect('http://localhost:3001')
sio.wait()

# sio.emit('data', 111)
