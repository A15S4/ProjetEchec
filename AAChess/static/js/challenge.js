// Code pour l'affichage de l'échiquier inspir de https://www.youtube.com/watch?v=Qv0fvm5B0EM&t=2903s

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


document.addEventListener("DOMContentLoaded", function() {

    let congradultions = ["Très bien!", "Bravo!", "Êtes-vous un Grandmaster?", "Super!", "Quelle efficacité!", "Impressionant!", "Trivial!", "Fantastique!"]
    randomNumber = Math.floor(Math.random()*congradultions.length);
  
    const gameboard = document.querySelector("#gameboard")
    const playerDisplay = document.querySelector("#player")
    const infoDisplay = document.querySelector("#info-display")

    let playerGo = ""
    turn_1 === "w" ? playerGo = "white" : playerGo = "black"
    "white" === playerGo ? playerDisplay.textContent = "blancs" : playerDisplay.textContent = "noirs"
    
    chessLetters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    chessNumbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
    function show_board(fen) {
        const start_pieces = convertFenToPieces(fen);
        let letterPosition = 0
        let numberPosition = 0
    
        gameboard.innerHTML = "";
        start_pieces.forEach((piece, i) => {
            let square = document.createElement("div");
            square.classList.add("square");
            square.setAttribute("square-id", i);
            const row = Math.floor((63 - i) / 8) + 1;

            if (row % 2 == 0) {
                square.classList.add(i % 2 == 0 ? "beige" : "brown");
            } else {
                square.classList.add(i % 2 == 0 ? "brown" : "beige");
            }
    
            switch (true) {
                case piece.toUpperCase() === "R":
                    square.innerHTML = rook;
                    break;
                case piece.toUpperCase() === "N":
                    square.innerHTML = knight;
                    break;
                case piece.toUpperCase() === "B":
                    square.innerHTML = bishop;
                    break;
                case piece.toUpperCase() === "Q":
                    square.innerHTML = queen;
                    break;
                case piece.toUpperCase() === "K":
                    square.innerHTML = king;
                    break;
                case piece.toUpperCase() === "P":
                    square.innerHTML = pawn;
                    break;
                default:
                    break;
            }
    
            if (piece !== "") {
                square.firstChild.setAttribute("draggable", true);

                if (piece.toUpperCase() === piece) {
                    square.firstChild.firstChild.classList.add("white");
                }
                if (piece.toLowerCase() === piece) {
                    square.firstChild.firstChild.classList.add("black");
                }
            }

            if (i % 8 == 0){
                let numberLabel = document.createElement("div");
                numberLabel.classList.add("number-label");
                numberLabel.innerText = chessNumbers[numberPosition++]; // Vous pouvez ajuster ce numéro comme vous le souhaitez
                square.appendChild(numberLabel);
                square.classList.contains('brown') ? numberLabel.classList.add('beigeE'):numberLabel.classList.add('brownE');
            }
            if (i >= 56){
                let letterLabel = document.createElement("div");
                letterLabel.classList.add("letter-label");
                letterLabel.innerText = chessLetters[letterPosition++]; // Vous pouvez ajuster ce numéro comme vous le souhaitez
                square.appendChild(letterLabel);
                square.classList.contains('brown') ? letterLabel.classList.add('beigeE'):letterLabel.classList.add('brownE');
            }
            gameboard.append(square);
        });

        const allSquares = document.querySelectorAll(".square")
        allSquares.forEach(square=>{
        square.addEventListener('dragstart', dragStart);
        square.addEventListener('dragover', dragOver);
        square.addEventListener('drop', dragDrop);
    });
    }
    
    function convertFenToPieces(fen) {
        const rows = fen.split("/");
        let start_pieces = [];
        rows.forEach((row) => {
            let emptyCount = 0;
            for (let i = 0; i < row.length; i++) {
                if (!isNaN(parseInt(row[i]))) {
                    emptyCount += parseInt(row[i]);
                } else {
                    if (emptyCount > 0) {
                        for (let j = 0; j < emptyCount; j++) {
                            start_pieces.push("");
                        }
                        emptyCount = 0;
                    }
                    start_pieces.push(row[i]);
                }
            }
            if (emptyCount > 0) {
                for (let j = 0; j < emptyCount; j++) {
                    start_pieces.push("");
                }
            }
        });
        return start_pieces;
    }

    show_board(board_1);
    let startPositionId
    let draggedElement

    function dragStart(e){
        startPositionId = e.target.parentNode.getAttribute('square-id')
        draggedElement = e.target
    }
    function dragOver(e){
        e.preventDefault() 
    }


    function dragDrop(e) {
        e.stopPropagation(); 
        const targetSquare = e.target.classList.contains('square') ? e.target : e.target.parentNode;
        const targetId = Number(targetSquare.getAttribute('square-id'));
        const correctGo = draggedElement.firstChild.classList.contains(playerGo); 
        const opponentGo = playerGo == 'white' ? 'black' : 'white';
        const takenByOpponent = e.target.firstChild?.classList.contains(opponentGo);
    
        if (correctGo) {
            targetSquare.appendChild(draggedElement);
            let currentBoardState = convertBoardToFen();

            if (currentBoardState != board_2) {
                targetSquare.removeChild(draggedElement);
                const startSquare = document.querySelector(`.square[square-id="${startPositionId}"]`);
                startSquare.appendChild(draggedElement);
    
                if (takenByOpponent) {
                    e.target.appendChild(e.target.firstChild);
                }
            } else {
                if (takenByOpponent) {
                    e.target.removeChild(e.target.firstChild);
                }
            }
        }
    }
    function dragDrop(e) {
        e.stopPropagation(); 
        const targetSquare = e.target.classList.contains('square') ? e.target : e.target.parentNode;
        const correctGo = draggedElement.firstChild.classList.contains(playerGo); 
        const opponentGo = playerGo == 'white' ? 'black' : 'white';
        const takenByOpponent = e.target.firstChild?.classList.contains(opponentGo);
        const taken = e.target.classList.contains("piece");
    
        if (taken && !takenByOpponent){
            infoDisplay.textContent = "Mauvais mouvement!";
            setTimeout(()=>infoDisplay.textContent = "", 2000);
            return
        }

        if (correctGo) {
            let capturedPiece = null;
            if (takenByOpponent) {
                capturedPiece = e.target.firstChild;
               e.target.parentNode.appendChild(draggedElement);
               e.target.remove();
            }
            else{
                targetSquare.appendChild(draggedElement);
            }
        
            fen = convertBoardToFen();
            let currentBoardState = convertBoardToFen();
            if (currentBoardState != board_2) {
                show_board(board_1)
                
            }
            else{
                setTimeout(()=>{

                    document.querySelector(".next").style.visibility = "visible";
                    document.querySelector("#gameboard").style.visibility = "hidden";
                    document.querySelector(".hint").style.display = "none";
                    document.querySelector(".next_text").innerText = congradultions[randomNumber]
                    document.querySelector(".clapping").style.visibility = "visible";
                }, 400);
            }
            
        
        }   
    }
    function convertBoardToFen() {
        let fen = '';
        let emptyCount = 0;

        let board = document.querySelectorAll('.square');
        
        for (let i = 0; i < board.length; i++) {
            let square = board[i];
            let piece = '';
            let pieceId = square.firstChild ? square.firstChild.getAttribute('id') : null;
        
            if (pieceId) {
                let svg = square.firstChild.firstChild;
                if (svg) {
                    if (pieceId === 'pawn') {
                        svg.classList.contains('white') ? piece = 'P' : piece = 'p';
                    } else if (pieceId === 'rook') {
                        svg.classList.contains('white') ? piece =  'R' : piece =  'r';
                    } else if (pieceId === 'knight') {
                        svg.classList.contains('white') ?  piece = 'N' : piece =  'n';
                    } else if (pieceId === 'bishop') {
                        svg.classList.contains('white') ? piece =  'B' : piece =  'b';
                    } else if (pieceId === 'queen') {
                        svg.classList.contains('white') ? piece =  'Q' : piece =  'q';
                    } else if (pieceId === 'king') {
                        svg.classList.contains('white') ? piece =  'K' : piece =  'k';
                    }
                }
            }
            if (piece !== '') {
                if (emptyCount > 0) {
                    fen += emptyCount.toString();
                    emptyCount = 0;
                }
                fen += piece;
            } else {
                emptyCount++;
            }

            if ((i + 1) % 8 === 0 && i !== 63) {
                if (emptyCount > 0) {
                    fen += emptyCount.toString();
                    emptyCount = 0;
                }
                fen += '/';
            }
        }

        if (emptyCount > 0) {
            fen += emptyCount.toString();
        }
    
        return fen;
    }


    function highlightMovedPiece(fen1, fen2) {

        let array1 = [];
        for (let i = 0; i < fen1.length; i++) {
            const element = fen1[i];
            if (!isNaN(element)) {
                for (let j = 0; j < element; j++) {
                    array1.push("");
                }
            } else {
                array1.push(element);
            }
        }
    
        let array2 = [];
        for (let i = 0; i < fen2.length; i++) {
            const element = fen2[i];
            if (!isNaN(element)) {
                for (let j = 0; j < element; j++) {
                    array2.push("");
                }
            } else {
                array2.push(element);
            }
        }
    
        for (let i = 0; i < array1.length; i++) {
            if (array1[i] !== array2[i]) {
                if (array2[i] == ""){
                    let id = 0
                    for (let k = 0; k < i; k++) {
                        if (array1[k] != "/"){
                            id ++
                        }
                    }
                    const square = document.querySelector(`.square[square-id="${id}"]`);
                    square.classList.add('highlight');
                }
            }
        }
    }

    
   document.querySelector(".hint").addEventListener("click", ()=>{
    highlightMovedPiece(board_1, board_2)
   });
    fen = convertBoardToFen()
});