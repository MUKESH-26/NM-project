// Global variables
let currentStep = 0;
const steps = [
    { question: "Hello! I'm your Road Accident Prediction Assistant. Would you like to make a prediction? (yes/no)" },
    { question: "Let's start with the weather condition. Is it: 1) Clear, 2) Rain, 3) Snow?" },
    { question: "What's the lighting condition? 1) Daylight, 2) Dark - Lighted, 3) Dark - Not Lighted" },
    // Add more steps as needed
];

function addMessage(message, isUser = false) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleUserInput(input) {
    const lowercaseInput = input.toLowerCase();
    
    if (currentStep === 0) {
        if (lowercaseInput === 'yes') {
            currentStep++;
            addMessage(steps[currentStep].question);
        } else if (lowercaseInput === 'no') {
            addMessage("Okay, let me know if you need anything else!");
        } else {
            addMessage("Please answer with 'yes' or 'no'.");
        }
        return;
    }
    
    // Handle other steps
    processInput(input);
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, true);
        handleUserInput(message);
        input.value = '';
    }
}

async function submitPrediction(predictionData) {
    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(predictionData)
        });
        
        const result = await response.json();
        
        if (result.error) {
            addMessage(`Error: ${result.error}`);
        } else {
            const predictionType = result.prediction === 1 ? "Severe" : "Non-severe";
            const probability = (result.probability * 100).toFixed(2);
            
            addMessage(`Based on the provided information, I predict this would be a ${predictionType} accident with ${probability}% confidence.`);
        }
    } catch (error) {
        addMessage(`Error making prediction: ${error.message}`);
    }
}

// Event listeners
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initialize chat
addMessage(steps[0].question);