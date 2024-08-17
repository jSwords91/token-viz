const inputArea = document.getElementById('input-area');
const tokenizerSelect = document.getElementById('tokenizer-select');
const tokenDisplay = document.getElementById('token-display');
const tokenCount = document.getElementById('token-count');
const errorMessage = document.getElementById('error-message');
const clearBtn = document.getElementById('clear-btn');
const colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#FFD9B3', '#E6B3FF'];
let colorIndex = 0;

function getNextColor() {
    const color = colors[colorIndex];
    colorIndex = (colorIndex + 1) % colors.length;
    return color;
}

function cleanDisplayToken(token) {
    // Remove or replace leading special characters
    let cleanToken = token.replace(/^[Ġ▁_Ċ]/, ' ');

    // Handle BERT's subword tokens
    if (cleanToken.startsWith('##')) {
        cleanToken = cleanToken.slice(2);
    }

    // Replace special tokens with more readble versions
    const specialTokens = {
        '[CLS]': '[START]',
        '[SEP]': '[END]',
        '[PAD]': '[PAD]',
        '[UNK]': '[UNKNOWN]'
    };

    cleanToken = cleanToken.replace('Ċ', '\n');

    return specialTokens[cleanToken] || cleanToken;
}

function displayToken(token) {
    const span = document.createElement('span');
    const cleanToken = cleanDisplayToken(token);

    span.textContent = cleanToken;
    span.className = 'token';
    span.style.backgroundColor = getNextColor();
    span.setAttribute('data-original', token); // Store original token for hover effect

    if (/^[^a-zA-Z0-9]/.test(token)) {
        span.style.marginLeft = '4px';
    }


    // Add subword-token class for BERT subwords
    if (token.startsWith('##')) {
        span.classList.add('subword-token');
    }

    tokenDisplay.appendChild(span);
}



async function updateTokens() {
    const text = inputArea.value;
    const tokenizer = tokenizerSelect.value;

    try {
        const response = await fetch('/api/tokenize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, tokenizer }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        tokenDisplay.innerHTML = '';
        errorMessage.textContent = '';
        data.tokens.forEach(displayToken);
        tokenCount.textContent = `Tokens: ${data.count}`;
    } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = `An error occurred: ${error.message}`;
        tokenDisplay.innerHTML = '';
        tokenCount.textContent = '';
    }
}



function clearText() {
    inputArea.value = '';
    tokenDisplay.innerHTML = '';
    errorMessage.textContent = '';
}

inputArea.addEventListener('input', updateTokens);
tokenizerSelect.addEventListener('change', updateTokens);
clearBtn.addEventListener('click', clearText);

// Initial load
updateTokens();