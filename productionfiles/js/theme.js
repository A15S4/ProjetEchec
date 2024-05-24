var themeOptions = ["scifi","classic","dark", "forest", "ocean","fire","ice"];
var themeNames = {
    scifi: "Sci-Fi",
    classic: "Classique",
    dark: "Sombre",
    forest: "Forêt",
    ocean: "Océan",
    fire: "Feu",
    ice: "Glace"
};
var themeIndex = themeOptions.indexOf(localStorage.getItem('theme')) !== -1 
                    ? themeOptions.indexOf(localStorage.getItem('theme')) 
                    : 0;

/* généré par chatgpt*/
function afficherTheme() {
    var elementAffiche = document.getElementById("themeAffiche");
    elementAffiche.innerHTML = themeNames[themeOptions[themeIndex]];
    document.documentElement.className = `theme-${themeOptions[themeIndex]}`;
    localStorage.setItem('theme', themeOptions[themeIndex]);
    if(document.querySelector("#player") !== null){
        if(document.querySelector("#player").textContent == 'blancs' || document.querySelector("#player").textContent == 'bleus'){
            if(localStorage.getItem('theme') === 'scifi'){
                document.querySelector("#player").textContent = "bleus";
            }
            else{
                document.querySelector("#player").textContent = 'blancs'
            }
        }
        if(document.querySelector("#player").textContent == 'noirs'|| document.querySelector("#player").textContent == 'rouges'){
            if(localStorage.getItem('theme') === 'scifi'){
                document.querySelector("#player").textContent = "rouges";
            }
            else{
                document.querySelector("#player").textContent = 'noirs'
            }
        }
        
    } 

    if(document.getElementById("colAffiche") !== null){
        if(localStorage.getItem('theme') === 'scifi'){
            colordiffOptions = ["Bleu", "Rouge"];
            afficherCol();
        }
        else{
            colordiffOptions = ["Blanc", "Noir"];
            afficherCol();
        }
    } 
}

function toggleThemeDiv() {
    var div = document.querySelector(".color_choice");
    if (div.style.display === "none") {
        div.style.display = "flex";
    } else {
        div.style.display = "none";
    }
}

function themePrecedent() {
    themeIndex = (themeIndex - 1 + themeOptions.length) % themeOptions.length;
    afficherTheme();
}

function themeSuivant() {
    themeIndex = (themeIndex + 1) % themeOptions.length;
    afficherTheme();
}

document.addEventListener('DOMContentLoaded', () => {
    afficherTheme();
    document.querySelector(".color_choice").style.display = 'none';
});