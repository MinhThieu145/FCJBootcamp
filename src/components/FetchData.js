
async function SendMessage(articleUrl) {    
    const ws = new WebSocket('wss://5fodc7y5ti.execute-api.us-east-1.amazonaws.com/production');

    // on message
    ws.onopen = () => {
        console.log('connected');

        // send the message
        ws.send(JSON.stringify({
            action: 'sendmessage',
            articleUrl: articleUrl
        }));
        
        // when receive a message
        ws.onmessage = (event) => {
            const result = JSON.parse(event);

            // log the result
            console.log(result);


        }
    }
}

