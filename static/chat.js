var source = new EventSource("/stream");

var p = document.createElement('p');
document.querySelector('#chat').appendChild(p);

//SSEの新しいイベントが発生した場合動作
source.onmessage = function(event) {
    if (event.data === '\n') {
        p = document.createElement('p');
        document.querySelector('#chat').appendChild(p);
    } else {
        p.textContent += event.data;
    }
};

document.querySelector('#form').addEventListener('submit', function(e) {
    e.preventDefault();
    p = document.createElement('p');
    document.querySelector('#chat').appendChild(p);
    var message = document.querySelector('#message').value + '\n';
    fetch('/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({message: message})
    });
    document.querySelector('#message').value = '';
});
