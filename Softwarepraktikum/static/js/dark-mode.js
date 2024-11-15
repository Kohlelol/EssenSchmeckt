document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const body = document.body;
    const toggleIcon = document.querySelector('.toggle-icon');
    const sunIcon = toggleIcon.getAttribute('data-sun-icon');
    const moonIcon = toggleIcon.getAttribute('data-moon-icon');

    const updateIcon = () => {
        if (body.classList.contains('dark-mode')) {
            toggleIcon.src = sunIcon;
        } else {
            toggleIcon.src = moonIcon;
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

    toggleButton.addEventListener('change', () => {
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