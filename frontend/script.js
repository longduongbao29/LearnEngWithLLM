
// Select elements from the DOM
const messageInput = document.getElementById('messageInput');
const chatBot = document.getElementById('chatbot');
const clearBtn = document.getElementById('clearBtn');
const ttsToggle = document.getElementById('ttsToggle');
const seachBtn = document.getElementById('seachBtn');
const seachInput = document.getElementById('seachInput');
const selectVoice = document.getElementById('selectVoice');
const sidebar = document.getElementById('setting');
const chatInterface = document.querySelector('.chat-interface');
const toggleSidebarBtn = document.getElementById('toggleSidebar');
// Assuming you have these HTML elements
const activitySelect = document.getElementById('activity');
const levelSelect = document.getElementById('level');
const topicSelect = document.getElementById('topic');
const sidebar_right = document.getElementById('dictionary');
const api = "/api/";
// Function to add a message to the chat
function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    chatBot.appendChild(messageDiv);
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'assistant-message');
    chatBot.scrollTop = chatBot.scrollHeight; // Scroll to the bottom
    const htmlArray = Array.from(message);
    let displayText = ''; // This will hold the progressively built HTML string

    // Typing effect with interval
    const typingInterval = setInterval(() => {
        if (htmlArray.length > 0) {
            displayText += htmlArray.shift(); // Add next character
            messageDiv.innerHTML = displayText; // Update message content
            chatBot.scrollTop = chatBot.scrollHeight; // Keep chat scrolled to bottom
        } else {
            clearInterval(typingInterval); // Stop when all characters are displayed
        }
    }, 30); // Adjust speed here by changing delay time (in milliseconds)
}


// Clear button functionality
clearBtn.addEventListener('click', () => {
    if (confirm("Are you sure you want to clear the chat?")) {
        chatBot.innerHTML = ''; // Clear the chat
    }
});

// Function to handle Text-to-Speech

// Select elements from the DOM

// Function to toggle sidebar visibility
toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    chatInterface.classList.toggle('expanded');
    // sidebar.classList.toggle('collapsed');
});




// Hàm để lấy giá trị



async function fetchAudio(input, voice,id) {
    const requestBody_audio = JSON.stringify({
        text: input,
        voice: voice
    });
    // console.log(requestBody_audio);

    fetch(api + "audio", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=UTF-8",
        },
        body: requestBody_audio,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok: " + response.statusText);
            }
            return response.json(); // Parse the JSON from the response
        })
        .then(data => {
            const audioPlayer = document.getElementById(id);
            audioPlayer.src = api + "audio/" + data.audio + "?t=" + new Date().getTime();
            audioPlayer.load();
            audioPlayer.play().catch(err => console.error("Audio playback failed:", err));
        })
        .catch(error => {
            console.error("Request failed:", error);
            addMessage("An error occurred while fetching the response.", 'assistant');
        });
    // Handle audio playback if "tts" is enabled

}


async function fetchFromAPI() {
    const activity = activitySelect.value;
    const level = levelSelect.value;
    const topic = topicSelect.value;
    const tts = ttsToggle.checked;
    const voice = selectVoice.value;
    const userMessage = messageInput.value;
    const messages = Array.from(chatBot.querySelectorAll('.message'))
    .slice(0, -1) // Bỏ qua tin nhắn cuối cùng
    .map(msg => ({
        role: msg.classList.contains('user-message') ? 'user' : 'assistant', // Xác định role dựa vào class
        content: msg.textContent.trim() // Lấy nội dung và xóa khoảng trắng
    }));
    console.log(messages);
    

    const requestBody = JSON.stringify({
        activity,
        level,
        topic,
        userMessage,
        chatHistory: messages
    });


    // Use fetch to make the API call
    fetch(api + "response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=UTF-8",
        },
        body: requestBody,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok: " + response.statusText);
            }
            return response.json(); // Parse the JSON from the response
        })
        .then(data => {
            
            // Add message to chat
            addMessage(data.text.replace(/```html/g, '').replace(/```/g, ''), 'assistant');
            if (tts) {
                fetchAudio(data.text, voice,'ttsAudio')
            }
        })
        .catch(error => {
            console.error("Request failed:", error);
            addMessage("An error occurred while fetching the response.", 'assistant');
        });


}
// Call this function when the user sends a message
messageInput.addEventListener('keypress', (event) => {
    // event.preventDefault();
    if (event.key === 'Enter' && messageInput.value.trim() !== '') {
        const userMessage = messageInput.value;
        addMessage(userMessage, 'user');
        fetchFromAPI(); // Fetch from API after sending the user message
        messageInput.value = ''; // Clear input
    }
});


function SearchDictionary(text) {
    const endpoint = "https://api.dictionaryapi.dev/api/v2/entries/en/"
     fetch(endpoint +  text, {
        method: "GET",
        headers: {
            "Content-Type": "application/json;charset=UTF-8",
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok: " + response.statusText);
            }
            return response.json(); // Parse the JSON from the response
        })
         .then(data => {
            const entry = data[0];
        
            document.getElementById('word').textContent = `Word: ${entry.word}`;

        // Hiển thị các phát âm
        const phoneticsList = document.getElementById('phonetics-list');
        phoneticsList.innerHTML = ''; // Xóa nội dung cũ
             entry.phonetics.forEach(phonetic => {
                 if (phonetic.audio) {
                const li = document.createElement('li');
            li.innerHTML = `
            <div id="phonetics-list">
                <div class="phonetic-item">
                    <span>${phonetic.text}</span>
                    <button class="play-audio" onclick="playAudio('${phonetic.audio}')">
                        <img src="https://cdn-icons-png.flaticon.com/128/10181/10181172.png" alt="Play Audio" />
                    </button>
            </div>
               
            `;
            phoneticsList.appendChild(li);
            }
            
        });

        // Hiển thị nghĩa
        const meaningsContainer = document.getElementById('meanings-container');
        meaningsContainer.innerHTML = ''; // Xóa nội dung cũ
        entry.meanings.forEach(meaning => {
            const partOfSpeech = document.createElement('h4');
            partOfSpeech.textContent = meaning.partOfSpeech;

            const definitionsList = document.createElement('ul');
            meaning.definitions.forEach(definition => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <p>Definition: ${definition.definition}</p>
                    ${definition.example ? `<p>Example: ${definition.example}</p>` : ''}
                `;
                definitionsList.appendChild(li);
            });

            meaningsContainer.appendChild(partOfSpeech);
            meaningsContainer.appendChild(definitionsList);
        });
        })
         .catch(error => {
             console.log(error);
              alert("Từ bạn tìm kiếm không được tìm thấy trong từ điển.");
        });

}

function speak(text) {
    const voice = selectVoice.value;
    SearchDictionary(text)

}

// Pronounce button functionality
seachBtn.addEventListener('click', () => {
    const pronunciationText = seachInput.value;
    if (pronunciationText) {
        speak(pronunciationText);
    }
});

function playAudio(audioSrc) {
    const audio = new Audio(audioSrc);
    audio.play().catch(err => console.error("Audio playback failed:", err));
}

const resizer = document.querySelector('.resizer');
// const sidebar_right = document.getElementById('sidebar-right');
let isResizing = false;

// Bắt đầu điều chỉnh kích thước khi nhấn chuộtlet isResizing = false;

resizer.addEventListener('mousedown', (event) => {
    isResizing = true;
    document.body.style.pointerEvents = 'none'; // Tạm thời vô hiệu hóa sự kiện con trỏ
});

document.addEventListener('mousemove', (event) => {
    if (isResizing) {
        const newWidth = event.clientX;
        // console.log(newWidth);
        const screenWidth = window.innerWidth;
        if (newWidth > 600 && newWidth < screenWidth) { // Giới hạn chiều rộng
            sidebar_right.style.width = `${screenWidth-newWidth}px`;
        }
    }
});

document.addEventListener('mouseup', () => {
    if (isResizing) {
        isResizing = false;
        document.body.style.pointerEvents = ''; // Kích hoạt lại sự kiện con trỏ
    }
});


function saveToLocalStorage(key, value) {
    localStorage.setItem(key, value);
}

// Function to load data from local storage
function loadFromLocalStorage(key, defaultValue = '') {
    return localStorage.getItem(key) || defaultValue;
}

// Save message input value


// Save tts toggle state
ttsToggle.addEventListener('change', () => saveToLocalStorage('ttsToggle', ttsToggle.checked));


// Save selected voice
selectVoice.addEventListener('change', () => saveToLocalStorage('selectVoice', selectVoice.value));

// Save activity, level, and topic selections
activitySelect.addEventListener('change', () => saveToLocalStorage('activitySelect', activitySelect.value));
levelSelect.addEventListener('change', () => saveToLocalStorage('levelSelect', levelSelect.value));
topicSelect.addEventListener('change', () => saveToLocalStorage('topicSelect', topicSelect.value));

// Load saved data from local storage on page load
window.addEventListener('load', () => {
    messageInput.value = loadFromLocalStorage('messageInput');
    ttsToggle.checked = JSON.parse(loadFromLocalStorage('ttsToggle', 'false'));
    seachInput.value = loadFromLocalStorage('seachInput');
    selectVoice.value = loadFromLocalStorage('selectVoice');
    if (JSON.parse(loadFromLocalStorage('sidebarHidden', 'false'))) {
        sidebar.classList.add('hidden');
    }
    activitySelect.value = loadFromLocalStorage('activitySelect');
    levelSelect.value = loadFromLocalStorage('levelSelect');
    topicSelect.value = loadFromLocalStorage('topicSelect');
});

// const chatInterface = document.querySelector('.chat-interface');

// Hàm để điều chỉnh chiều cao của chat interface
function adjustChatInterfaceHeight() {
    // Cập nhật chiều cao chat interface
    chatInterface.style.height = `calc(100vh)`; // Điều chỉnh chiều cao theo nhu cầu
}

window.addEventListener('resize', adjustChatInterfaceHeight);

// Gọi hàm ban đầu
adjustChatInterfaceHeight();