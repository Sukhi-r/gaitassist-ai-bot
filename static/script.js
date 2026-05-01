document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    alert('Script loaded!');  // Temporary alert to check if JS loads
    const inputField = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatbox = document.getElementById('chatbox');

    console.log('Elements found:', inputField, sendBtn, chatbox);
    if (!inputField) console.error('inputField not found!');
    if (!sendBtn) console.error('sendBtn not found!');
    if (!chatbox) console.error('chatbox not found!');

    function addMessage(content, sender = 'bot', showConfidence = false, confidence = 0) {
        const message = document.createElement('div');
        message.className = 'message ' + sender;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = sender === 'user' ? '👤' : '🤖';

        const text = document.createElement('div');
        text.className = 'text';
        let confidenceHtml = '';
        if (showConfidence) {
            confidenceHtml = `<br/><span class="confidence">Confidence: ${confidence}%</span>`;
        }
        text.innerHTML = content + confidenceHtml;

        message.appendChild(avatar);
        message.appendChild(text);
        chatbox.appendChild(message);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function getHelp() {
        console.log('getHelp called');
        addMessage("I need help", 'user');

        fetch('/get', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: "help" })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Help response:', data);
            addMessage(data.reply, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        });
    }

    function sendMessage() {
        console.log('sendMessage called');
        if (!inputField) {
            console.error('inputField not found');
            return;
        }
        const text = inputField.value.trim();
        console.log('Input text:', text);
        if (!text) {
            console.log('No text, returning');
            return;
        }

        addMessage(text, 'user');
        inputField.value = '';

        fetch('/get', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);
            addMessage(data.reply, 'bot', true, data.confidence || 0);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        });
    }

    sendBtn.addEventListener('click', function() {
        console.log('Send button clicked, input value:', inputField ? inputField.value : 'inputField null');
        sendMessage();
    });
    inputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            console.log('Enter pressed');
            event.preventDefault();
            sendMessage();
        }
    });

    // Make getHelp available globally
    window.getHelp = getHelp;
});
</content>
<parameter name="filePath">c:\Sukhi\chatbot\static\script.js