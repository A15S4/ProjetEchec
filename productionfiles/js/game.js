// Code pour l'affichage de l'échiquier inspir de https://www.youtube.com/watch?v=Qv0fvm5B0EM&t=2903s
let boardData;
let playerGo;
let start_pieces;
let startPositionId;
let draggedElement;
let start = false;
let gameboard;
let playerDisplay;
let allSquares;
let pieceSymbols;
let tempBoard;
let startSquareId = null;
let currentPlayerColor;
const initialBoard = [
    "bR1", "bN1", "bB1", "bQ1", "bK1", "bB2", "bN2", "bR2",
    "bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7", "bP8",
    "wP1", "wP2", "wP3", "wP4", "wP5", "wP6", "wP7", "wP8",
    "wR1", "wN1", "wB1", "wQ1", "wK1", "wB2", "wN2", "wR2"
];
const capturedPiecesBlack = [];
const capturedPiecesWhite = [];
const addedPieces = [];
const chessLettersW = ["a", "b", "c", "d", "e", "f", "g", "h"];
const chessNumbersW = ["8", "7", "6", "5", "4", "3", "2", "1"];
const chessLettersB = ["h", "g", "f", "e", "d", "c", "b", "a"];
const chessNumbersB = ["1", "2", "3", "4", "5", "6", "7", "8"];

document.addEventListener("DOMContentLoaded", function() {
    gameboard = document.querySelector("#gameboard");
    pieceSymbols = {
        'R': rook,
        'N': knight,
        'B': bishop,
        'Q': queen,
        'K': king,
        'P': pawn
    };
    document.querySelector(".back").onclick = function() {
        window.location.href = "/lobby/";
    };
    document.querySelector(".yes").onclick = function() {
        quit();
    };
    document.querySelector(".no").onclick = function() {
        document.querySelector(".exit-box").style.display = 'none';
    };
    setTimeout(state, 1000);
});

/*permet de récupérer la valeur d'un cookie spécifique à partir des cookies stockés dans le navigateur,
tels que le jeton CSRF dans ce cas précis.  Généré par ChatGPT*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function updateCapturedPieces(initialBoard, currentBoard) {
    for (const piece of initialBoard) {
        if (!currentBoard.includes(piece) && !addedPieces.includes(piece)) {
          if (piece.startsWith('b')) {
            capturedPiecesBlack.push(piece);
          } else if (piece.startsWith('w')) {
            capturedPiecesWhite.push(piece);
          }
          addedPieces.push(piece); 
        }
      }
}

function updateText(capturedPieces) {
    return capturedPieces.length > 0 ? capturedPieces.join(', ') : '';
}

function renderCapturedPieces(capturedPieces, targetElementId) {
    const piecesContainer = document.querySelector(`#${targetElementId}`);
    piecesContainer.innerHTML = '';
  
    capturedPieces.forEach(pieceCode => {
        const pieceDiv = document.createElement("div");
        const container = document.createElement("div");
        container.classList.add("container");
        if (pieceCode.includes('b')) {
            pieceDiv.classList.add("black");
        } else if (pieceCode.includes('w')) {
            pieceDiv.classList.add("white");
        }
        if (pieceSymbols[pieceCode.charAt(1)]) {
            pieceDiv.innerHTML = pieceSymbols[pieceCode.charAt(1)];
        }
        container.appendChild(pieceDiv);
        piecesContainer.appendChild(container);
    });
}

function create_square(index, content,color,i) {
    const caseDiv = document.createElement('div');
    caseDiv.classList.add('square');
    caseDiv.setAttribute('square-id', index);

    const row = Math.floor((63 - index) / 8) + 1;
    const isEvenRow = row % 2 === 0;
    const isEvenIndex = index % 2 === 0;

    if ((isEvenRow && isEvenIndex) || (!isEvenRow && !isEvenIndex)) {
        caseDiv.classList.add('beige');
    } else {
        caseDiv.classList.add('brown');
    }
    if (content.includes('b')) {
        caseDiv.classList.add('black');
    } else if (content.includes('w')) {
        caseDiv.classList.add('white');
    }
    if (content !== '' && caseDiv.classList.contains(color)) {
        const pieceCode = content.charAt(1);
        const pieceSymbol = pieceSymbols[pieceCode];
        caseDiv.innerHTML = pieceSymbol;
        caseDiv.firstChild.setAttribute('draggable', true);
        caseDiv.firstChild.style.cursor = 'pointer';
    } else if(content !== ''){
        const pieceCode = content.charAt(1);
        const pieceSymbol = pieceSymbols[pieceCode];
        caseDiv.innerHTML = pieceSymbol;
    }
    return caseDiv;
}

function afficherEchiquier(echiquier,color) {
    const echiquierDiv = document.getElementById('gameboard');
    echiquierDiv.innerHTML = ''; 
    let letterPosition = 0
    let numberPosition = 0
    const iterate = (color == 'white') ? i => i : i => echiquier.length - 1 - i;
        for (let i = 0; i < echiquier.length; i++) {
            const index = iterate(i);
            const caseContent = echiquier[index];
            const caseDiv = create_square(index, caseContent,color,i);
            echiquierDiv.appendChild(caseDiv);
            if (i % 8 == 0){
                let numberLabel = document.createElement("div");
                numberLabel.classList.add("number-label");
                if(color =="white"){
                    numberLabel.innerText = chessNumbersW[numberPosition++]; 
                }
                else{
                    numberLabel.innerText = chessNumbersB[numberPosition++]; 
                }
                caseDiv.classList.contains('brown') ? numberLabel.classList.add('beigeE'):numberLabel.classList.add('brownE');
                caseDiv.appendChild(numberLabel);
            }
            if (i >= 56){
                let letterLabel = document.createElement("div");
                letterLabel.classList.add("letter-label");
                if(color =="white"){
                    letterLabel.innerText = chessLettersW[letterPosition++];
                }
                else{
                    letterLabel.innerText = chessLettersB[letterPosition++];
                }
                caseDiv.classList.contains('brown') ? letterLabel.classList.add('beigeE'):letterLabel.classList.add('brownE');
                caseDiv.appendChild(letterLabel);
            }
        }
}

function getPlayersByUsername(gameData, username) {
    if (gameData.player1.username === username) {
        return {
            player: gameData.player1,
            enemy: gameData.player2,  
        };
    } else if (gameData.player2.username === username) {
        return {
            player: gameData.player2,
            enemy: gameData.player1,  
        };
    } else {
        return {
            player: null,
            enemy: null
        };
    }
}

function getActivePlayerUsername(gameData) {
    if (gameData.player1.player_turn) {
        return gameData.player1.username;
    } else if (gameData.player2.player_turn) {
        return gameData.player2.username;
    } else {
        return null;
    }
}

function convertSecondsToTime(seconds) {
    if(seconds == 999){
        return 'illimité'
    }
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const formattedSeconds = remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds;

    return `${minutes}:${formattedSeconds}`;
}

const action = (startPosition,endPosition) =>{
    const csrftoken = getCookie('csrftoken');

    fetch('/action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'start': startPosition,'end': endPosition })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  
}    

const state = () => {
    fetch('/game_data/')
        .then(response => response.json())
        .then(game_data => {
            const data = game_data['data'];
            console.log(data);
            if (data == "WAITING") {
                start = false;
            }
            else if(data == "WON" || data == "LOST" || data == "DRAW"){
                setTimeout(() => {
                    document.querySelector(".end-box").style.display="flex";
                }, 1000);
                
                if(data == "WON"){
                    document.querySelector(".end-text").innerText="Vous avez gagné!";
                }
                else if(data == "LOST"){
                    document.querySelector(".end-text").innerText="Vous avez perdu!";
                }
                else{
                    document.querySelector(".end-text").innerText="Match nul!";
                }
            }
            else {
                if(start == false){
                    animIntro();
                }
                const players = getPlayersByUsername(data, username); 
                const playerInfo = players.player;
                const enemyInfo = players.enemy;
                const playerCapturedPieces = (playerInfo.color === 'white') ? capturedPiecesWhite : capturedPiecesBlack;
                const enemyCapturedPieces = (enemyInfo.color === 'white') ? capturedPiecesWhite : capturedPiecesBlack;
                currentPlayerColor = playerInfo.color;
                document.querySelector("#playerT").innerText = "Temps: " + convertSecondsToTime(playerInfo.time_left);
                document.querySelector("#enemyT").innerText = "Temps: " + convertSecondsToTime(enemyInfo.time_left);
                
                if (data['board'] && JSON.stringify(data['board']) !== JSON.stringify(tempBoard)) {
                    tempBoard = data['board'];
                    gameboard.innerHTML = '';
                    updateCapturedPieces(initialBoard,data['board'])
                    document.querySelector("#playerN").innerText = 'Joueur: ' + playerInfo.username;
                    document.querySelector("#enemyN").innerText = 'Adversaire: ' + enemyInfo.username;
                    document.querySelector(".gameType").innerText = 'Type de Partie: ' + data.game_type;
                    document.querySelector(".turn").innerText = "C'est au tour de "+getActivePlayerUsername(data)+" à jouer";
                    renderCapturedPieces(playerCapturedPieces, 'enemyP');
                    renderCapturedPieces(enemyCapturedPieces, 'playerP');
                    afficherEchiquier(data['board'], currentPlayerColor);
                    attachDragEventListeners();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    setTimeout(state, 1000);
}

const attachDragEventListeners = () => {
    const allSquares = document.querySelectorAll(".square");
    allSquares.forEach(square => {
        square.removeEventListener('dragstart', dragStart);
        square.removeEventListener('dragover', dragOver);
        square.removeEventListener('drop', dragDrop);
        square.removeEventListener('click', squareClick);

        square.addEventListener('dragstart', dragStart);
        square.addEventListener('dragover', dragOver);
        square.addEventListener('drop', dragDrop);
        square.addEventListener('click', squareClick);
    });
}


function dragStart(e){
    startPositionId = e.target.parentNode.getAttribute('square-id')
    draggedElement = e.target
    
}
function dragOver(e){
    e.preventDefault()    
}

function dragDrop(e) {
    e.stopPropagation(); 
    const targetId = Number(e.target.getAttribute('square-id')) || Number(e.target.parentNode.getAttribute('square-id'))
    const startId = Number(startPositionId);
    const startPosition = getPosition(startId);
    const endPosition = getPosition(targetId);
    action(startPosition,endPosition);
}

function getPosition(ID) {
    if (ID < 0 || ID > 63) {
        return "ID invalide";
    }
    var row = Math.floor(ID / 8); 
    var col = ID % 8; 
    return [row, col];
}

function squareClick(e) {
    const clickedSquareId = Number(e.target.getAttribute('square-id')) || Number(e.target.parentNode.getAttribute('square-id'));
    
    if (startSquareId === null) {
        const piece = e.target.parentNode.getAttribute('square-id');
        const pieceColor = e.target.parentNode.classList;
        if (piece && pieceColor.contains(currentPlayerColor) ) {
            startSquareId = clickedSquareId;
            e.target.parentNode.classList.add('highlight'); 
        }
    } else {
        const startPosition = getPosition(startSquareId);
        const endPosition = getPosition(clickedSquareId);
        action(startPosition, endPosition);
        startSquareId = null; 
        const highlightedSquare = document.querySelector('.highlight');
        if (highlightedSquare) {
            highlightedSquare.classList.remove('highlight'); 
        }
    }
}

function animIntro() {
    var element = document.querySelector(".loading");
    var opacity = 1;
    var intervalId = setInterval(function () {
      if (opacity > 0) {
        opacity -= 0.02; 
        element.style.opacity = opacity;
      } else {
        clearInterval(intervalId);
        element.style.display = 'none';
      }
    }, 20); 
}

const quit = () => {
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
        else{
            window.location.href = "/lobby/";
        }
    })
    .catch(error => {
        console.error('Erreur lors de la suppression de l\'utilisateur de la liste d\'attente:', error);
    });
}

function preQuit() {
    document.querySelector(".exit-box").style.display = 'flex';
}