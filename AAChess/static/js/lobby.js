var diffOptions = ["Facile", "Normal", "Difficile"];
var diffIndex = 0;
var colordiffOptions = ["Blanc", "Noir"];
var colorIndex = 0;

window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        fetch('/remove_from_list/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('La requête au serveur a échoué');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la suppression de l\'utilisateur de la liste d\'attente:', error);
        });
    }
});

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

function toggleDiv() {
    var div = document.querySelector(".box");
    if (div.style.display === "none") {
      div.style.display = "flex";
    } else {
      div.style.display = "none";
    }
}

function afficherCol() {
  var elementAffiche = document.getElementById("colAffiche");
  elementAffiche.innerHTML = colordiffOptions[colorIndex];
}

function colPrecedent() {
    colorIndex = (colorIndex - 1 + colordiffOptions.length) % colordiffOptions.length;
    afficherCol();
}
  
function colSuivant() {
    colorIndex = (colorIndex + 1) % colordiffOptions.length;
    afficherCol();
}

function afficherDiff() {
  var elementAffiche = document.getElementById("diffAffiche");
  elementAffiche.innerHTML = diffOptions[diffIndex];
}

function diffPrecedent() {
    diffIndex = (diffIndex - 1 + diffOptions.length) % diffOptions.length;
    afficherDiff();
}
  
function diffSuivant() {
    diffIndex = (diffIndex + 1) % diffOptions.length;
    afficherDiff();
}

document.addEventListener("DOMContentLoaded", function() {
    afficherCol();
    afficherDiff();
    document.querySelector(".box").style.display = 'none';
    document.getElementById("training").addEventListener("submit", function(event) {
    
        var couleurPiece = document.getElementById("colAffiche").textContent;
        var difficulte = document.getElementById("diffAffiche").textContent;
        if(couleurPiece === 'Rouge'){
            couleurPiece = 'Noir';
        }
        if(couleurPiece === 'Bleu'){
            couleurPiece = 'Blanc';
        }
    
        document.getElementById("couleur_piece").value = couleurPiece;
        document.getElementById("difficulte").value = difficulte;
    
        this.submit();
    });
});