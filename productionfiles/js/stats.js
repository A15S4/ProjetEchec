
// Fonction pour obtenir le jeton CSRF du cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Cherchez le cookie contenant le jeton CSRF
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const state = () =>{
    fetch('/game_data/')
    .then(response => response.json())
    .then(data => {
        console.log(data['data']['board']);
       
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    setTimeout(state, 1000);
}

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(state, 2000);
});
