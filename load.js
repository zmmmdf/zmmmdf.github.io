fetch('./dist/cses_cards.html')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        document.getElementById('pills-cses').innerHTML = `<div class="d-flex flex-row justify-content-center align-items-center flex-wrap">${html}</div>;`;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

fetch('./dist/eolymp_cards.html')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        document.getElementById('pills-eolymp').innerHTML = `<div class="d-flex flex-row justify-content-center align-items-center flex-wrap">${html}</div>;`
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
