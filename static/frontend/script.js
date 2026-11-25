const API_URL = 'http://127.0.0.1:8000';
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// মেসেজ দেখানোর ফাংশন
function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'user' ? 'message user-message' : 'message bot-message';
    msgDiv.innerHTML = text; 
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// কুইক বাটনের জন্য ফাংশন
function sendQuick(text) {
    userInput.value = text;
    sendMessage();
}

// মূল সেন্ড ফাংশন
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    appendMessage('user', message);
    userInput.value = '';
    
    // টাইপিং ইন্ডিকেটর
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.innerText = 'Typing...';
    chatBox.appendChild(loadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        loadingDiv.remove(); // Typing... মুছে ফেলা
        appendMessage('bot', data.reply);
    } catch (error) {
        loadingDiv.remove();
        appendMessage('bot', 'Error: Could not reach the server.');
        console.error('Error:', error);
    }
}

// ইভেন্ট লিসেনার
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});