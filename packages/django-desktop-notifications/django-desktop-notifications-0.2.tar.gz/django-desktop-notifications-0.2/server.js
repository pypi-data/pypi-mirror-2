/* Minimum time between 2 notifications of the same "notification_id" */
/* (in milliseconds) */
const MINIMUM_TIME_BETWEEN_NOTIFICATION = 30000;

var http = require('http'),
    https = require('https'),
    io = require('socket.io'),
    fs = require('fs'),
    dgram = require('dgram');

var server_sessions = {};
var notifications_backlog = {};

//var server = https.createServer({
//        key: fs.readFileSync(__dirname + '/key.pem'),
//        cert: fs.readFileSync(__dirname + '/cert.pem')
//    },
//    send_wsonly
//);
server = http.createServer(send_wsonly);

/* UDP4 Server initialization */
var udpserver = dgram.createSocket("udp4");
udpserver.on("listening", function() 
    {
        var address = udpserver.address();
        console.log("[UDPServer] listening " + address.address + ":"+address.port);
    }
);
udpserver.on("message", function(msg, rinfo)
    {
        var data;
        console.log("[UDPServer] received: " + msg + " from " +
            rinfo.address + ":" + rinfo.port);
        
        /* deserialize */
        try
        {
            data = JSON.parse(msg);
        } catch (e) {
            console.error("[UDPServer]: Unable to parse message: " + e);
            return null;
        }
        
        if (data && data.action == "notification")
            handle_udp_server_message(data);
    }
);
udpserver.bind(8011);
    
function send_wsonly(req, res)
{
    res.writeHeader(403);
    res.write('403, only websocket allowed.');
    res.end();
}

server.listen(8010);

var socket = io.listen(server);
socket.on('connection', function(client) 
{
    console.log("[Socket.IO] New connection received: "+client);
    client.on('message', function( evt )
    {
        var data;
        
        /* Log */
        console.log("[Socket.IO] Message received from "+client.sessionId+": "+evt);
        
        /* Parse */
        try {
            data = JSON.parse(evt);
        } catch (e) {
            console.error("[Socket.IO] Unable to parse message: " + e);
        }
        
        /* Handle */
        if (data) 
        {
            if (data.action && data.action == "register")
            {
                var username = data.username;
                var session = createOrUpdateSession(username, client);
                if (session)
                    console.log("[Socket.IO] Registered: " + session.toString());
            }
        }
    });
});

function handle_udp_server_message(data)
{
    var notification = {
        id: data.username + data.notification_id,
        username: data.username,
        notification_id: data.notification_id,
        tag: data.tag,
        autoclose_delay: data.autoclose_delay,
        original_data: data,
        send: function() {
            var session = getSession(data.username);
            if (! session)
            {
                console.log("Unable send message: no session found for username: "+ data.username);
            } else {
                session.send({
                    action: "notification", 
                    id_notification: notification.notification_id,
                    autoclose_delay: notification.autoclose_delay,
                    tag: notification.tag
                });
            }
        },
        destroy: function() { 
            delete notifications_backlog[notification.id];
        },
        timestamp: new Date(),
        poke: function() { notification.timestamp = new Date(); }
    };
    
    var do_send = true;
    /* Search for notifications of this username */
    for (var i in notifications_backlog)
    {
        var notif = notifications_backlog[i];
        if (notif.username == notification.username)
        {
            if (notif.notification_id == notification.notification_id)
            {
                console.log("Notif found: " + (notification.timestamp.getTime() - notif.timestamp.getTime()));
                /* Update the timestamp */
                if ((notification.timestamp.getTime() - notif.timestamp.getTime()) >= 
                    MINIMUM_TIME_BETWEEN_NOTIFICATION)
                {
                    /* Send the real notification */
                    notif.send();
                }
                do_send = false;
                break;
                notif.poke();
            }
        }
    }
    
    if (do_send)
    {
        console.log("No notification found...");
        notification.send();
        notifications_backlog[notification.id] = notification;
    }
}

/* Register the user in the sessionList, in order to send
 * only messages for this username */
function createOrUpdateSession(username, client)
{
    if (!username)
        return null;
    /* Check if the user is already registered */
    var session;
    for (var i in server_sessions)
    {
        session = server_sessions[i];
        if (session && session.username == username)
        {
            session.clients.push(client);
            session.poke();
        }
    }
    if (! session)
    {
        session = {
            /* LC: Is it unique for the running session ? */
            id: client.sessionId,
            username: username,
            clients: [ client ],
            last_seen: new Date(),
            poke: function() { session.last_seen = new Date(); },
            destroy: function() { delete server_sessions[session.id]; },
            toString: function() { 
                return "<" + session.username + "> " +
                    "(" + session.clients.length + " connected)";
            },
            send: function(message) {
                var data_serialized = JSON.stringify(message);
                for (var i in session.clients)
                {
                    var client = session.clients[i];
                    console.log("[Socket.IO] Sending to " + client + " message: " + data_serialized);
                    client.send(data_serialized);
                }
            }
        }
        server_sessions[session.id] = session;
    }
    return session;
}

/* Returns the list of sessions for this username */
function getSession(username)
{
    var ret = [];
    for (var i in server_sessions)
    {
        var session = server_sessions[i];
        if (session.username == username)
            return session;
    }
    return null;
}
