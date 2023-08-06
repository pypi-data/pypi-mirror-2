var ws = require("websocket-server");

var server = ws.createServer();

server.addListener("connection", function(connection)
{
    connection.addListener("message", function(msg)
    {
        console.log("Message received: "+msg);
        connection.send(msg);
    });
});

server.listen(8010);
