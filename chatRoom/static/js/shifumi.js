document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

const roomName = JSON.parse(document.getElementById('room-name').textContent);
let user = (Math.random() + 1).toString(36).substring(7);
let has_played = false;
console.log("random", user);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

const gameSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/shifumi/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').scrollTop = document.querySelector('#chat-log').scrollHeight;
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

gameSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data, has_played)
    if (has_played === true){
        document.querySelectorAll("button").forEach(e => {e.style.pointerEvents = "none"});
        has_played = false;
    } else {
        document.querySelector('#chat-message-input').focus();
        document.querySelectorAll("button").forEach(e => {
            e.style.pointerEvents="all";
            e.style.boxShadow = "5px -10px #33332D";
            e.style.backgroundColor = 'white' ;
            e.style.color = '#33332D';
        });
    };
    if (data.action !== "message"){
        document.querySelector('#chat-log').scrollTop = document.querySelector('#chat-log').scrollHeight;
        document.querySelector('#chat-log').value += ('you ' + data.action + '\n');
    };
}

gameSocket.onclose = function(e) {
    console.error('Game socket closed unexpectedly');
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'user': user,
        'message': message
    }));
    messageInputDom.value = '';
};

document.querySelectorAll('button').forEach(button => {
    button.onclick = (b) => {
        has_played = true;
        button.style.boxShadow = "5px -10px #e7e7e4";
        button.style.backgroundColor = '#33332D' ;
        button.style.color = 'white';
        gameSocket.send(JSON.stringify({
            'event': 'PLAY',
            'user': user,
            'play': button.innerHTML
        }));
    }
});
