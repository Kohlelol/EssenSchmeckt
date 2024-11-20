document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const body = document.body;
    const toggleIcon = document.querySelector('.toggle-icon-button');
    const sunIcon = toggleIcon.getAttribute('data-sun-icon');
    const moonIcon = toggleIcon.getAttribute('data-moon-icon');

    const updateIcon = () => {
        if (body.classList.contains('dark-mode')) {
            toggleIcon.src = sunIcon;
            console.log(toggleIcon.src)
        } else {
            toggleIcon.src = moonIcon;
            console.log(toggleIcon.src)
        }
    };


    if (localStorage.getItem('dark-mode') === 'enabled') {
        body.classList.add('dark-mode');
        toggleButton.checked = true;
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        toggleButton.checked = false;
    }

    
    document.getElementById('body').style.display = 'block';
    updateIcon();

    toggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        body.classList.toggle('light-mode');

        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.setItem('dark-mode', 'disabled');
        }
        updateIcon();
    });
});



const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        const query = this.value;
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/database/list/?q=${query}`, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 400) {
                const results = document.getElementById('results');
                const parser = new DOMParser();
                const doc = parser.parseFromString(xhr.responseText, 'text/html');
                results.innerHTML = doc.getElementById('results').innerHTML;
            }
        };
        xhr.send();
    });
};