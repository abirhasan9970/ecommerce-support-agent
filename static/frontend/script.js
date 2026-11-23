const chatWindow = document.getElementById('chat-window');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const modalOverlay = document.getElementById('modal-overlay');

// --- Chat Functions ---
function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    // marked.parse ব্যবহারের জন্য HTML-এ marked.js লাইব্রেরি থাকতে হবে
    contentDiv.innerHTML = marked.parse(text);
    
    msgDiv.appendChild(contentDiv);
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to bottom
}

async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    messageInput.value = '';
    
    // Show loading
    addMessage("Thinking...", 'bot');
    const loadingMsg = chatWindow.lastElementChild;
    
    try {
        // এখানে API_URL বাদ দিয়ে শুধু '/chat' দেওয়া হয়েছে
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        if (!response.ok) throw new Error("Server error");
        
        const data = await response.json();
        
        chatWindow.removeChild(loadingMsg); // Remove loading
        addMessage(data.reply, 'bot');
    } catch (error) {
        console.error(error);
        if (loadingMsg.parentNode) chatWindow.removeChild(loadingMsg);
        addMessage("Error: Could not reach the server.", 'bot');
    }
}

function sendQuickMessage(text) {
    messageInput.value = text;
    sendMessage();
}

function handleEnter(event) {
    if (event.key === 'Enter') sendMessage();
}

// --- Modal Functions ---
function openModal(type) {
    modalOverlay.classList.remove('hidden');
    
    // Hide all forms first
    document.getElementById('form-order').classList.add('hidden');
    document.getElementById('form-recommend').classList.add('hidden');
    document.getElementById('form-ticket').classList.add('hidden');
    
    // Clear results
    document.getElementById('order-result').innerText = '';
    document.getElementById('recommend-result').innerText = '';
    document.getElementById('ticket-result').innerText = '';
    
    // Show requested form
    if (type === 'order') document.getElementById('form-order').classList.remove('hidden');
    if (type === 'recommend') document.getElementById('form-recommend').classList.remove('hidden');
    if (type === 'ticket') document.getElementById('form-ticket').classList.remove('hidden');
}

function closeModal() {
    modalOverlay.classList.add('hidden');
}

// --- Order Tracking ---
async function submitOrder() {
    const orderId = document.getElementById('order-id-input').value;
    const resBox = document.getElementById('order-result');
    resBox.innerHTML = "Loading...";
    
    try {
        const response = await fetch('/track-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_id: orderId })
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            resBox.innerHTML = `<strong>Status:</strong> ${data.order.status}<br>
                                <strong>Est. Delivery:</strong> ${data.order.estimated_delivery}<br>
                                <strong>Items:</strong> ${data.order.items_summary}`;
        } else {
            resBox.innerHTML = `<span style="color: #ef4444;">${data.error}</span>`;
        }
    } catch (e) {
        resBox.innerText = "Error connecting to server.";
    }
}

// --- Product Recommendation ---
async function submitRecommend() {
    const price = parseFloat(document.getElementById('budget-input').value);
    const category = document.getElementById('category-input').value;
    const resBox = document.getElementById('recommend-result');
    resBox.innerHTML = "Searching...";
    
    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ max_price: price, category: category })
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            let html = '';
            data.products.forEach(p => {
                html += `<div style="margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 4px;">
                            <strong>${p.name}</strong> - ${p.price} BDT<br>
                            <span style="font-size: 0.8rem; color: #94a3b8;">${p.specifications}</span>
                         </div>`;
            });
            resBox.innerHTML = html;
        } else {
            resBox.innerHTML = `<span style="color: #f59e0b;">${data.message}</span>`;
        }
    } catch (e) {
        resBox.innerText = "Error connecting to server.";
    }
}

// --- Support Ticket ---
async function submitTicket() {
    const name = document.getElementById('ticket-name').value;
    const issue = document.getElementById('ticket-issue').value;
    const message = document.getElementById('ticket-message').value;
    const resBox = document.getElementById('ticket-result');
    
    if (!name || !message) {
        resBox.innerHTML = `<span style="color: #ef4444;">Name and message are required.</span>`;
        return;
    }

    resBox.innerHTML = "Creating ticket...";
    
    try {
        const response = await fetch('/support-ticket', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customer_name: name, message: message, issue_type: issue || "General" })
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            resBox.innerHTML = `<span style="color: #10b981;">Success!</span><br>${data.message}`;
        } else {
            resBox.innerHTML = `<span style="color: #ef4444;">${data.error}</span>`;
        }
    } catch (e) {
        resBox.innerText = "Error connecting to server.";
    }
}