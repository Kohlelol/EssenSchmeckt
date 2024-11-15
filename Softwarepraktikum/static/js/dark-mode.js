const toggleButton = document.getElementById('dark-mode-toggle');
        const body = document.body;

        if (localStorage.getItem('dark-mode') === 'enabled') {
            body.classList.add('dark-mode');
            toggleButton.checked = true;
        } else {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            toggleButton.checked = false;
        }
        window.addEventListener('load', function () {
             document.getElementById('body').style.display = 'block';
        })


        toggleButton.addEventListener('change', () => {
            body.classList.toggle('dark-mode');
            body.classList.toggle('light-mode');

            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('dark-mode', 'enabled');
            } else {
                localStorage.setItem('dark-mode', 'disabled');
            }
        });