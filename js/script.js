document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const hiraganaGrid = document.getElementById('hiragana-grid');
    const katakanaGrid = document.getElementById('katakana-grid');

    // Load data from data.json
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            renderGrid(data.hiragana, hiraganaGrid, 'assets/hiragana/');
            renderGrid(data.katakana, katakanaGrid, 'assets/katakana/');
        })
        .catch(err => console.error('Error loading data:', err));

    function renderGrid(items, gridElement, imagePathPrefix) {
        gridElement.innerHTML = '';
        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card';
            
            const imageWrapper = document.createElement('div');
            imageWrapper.className = 'card-image-wrapper';
            
            const img = document.createElement('img');
            img.src = imagePathPrefix + item.image;
            img.alt = 'Japanese Character Mnemonic';
            img.loading = 'lazy';
            
            imageWrapper.appendChild(img);
            
            const content = document.createElement('div');
            content.className = 'card-content';
            
            const mnemonic = document.createElement('p');
            mnemonic.className = 'card-mnemonic';
            mnemonic.textContent = item.mnemonic;
            
            content.appendChild(mnemonic);
            card.appendChild(imageWrapper);
            card.appendChild(content);
            gridElement.appendChild(card);
        });
    }

    // Tab switching logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked button and target content
            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});
