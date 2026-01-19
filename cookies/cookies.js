var cookies = 0
var four = 1
var usines = 1
var cookies_total = 0
function cookiesFunc() {
  cookies = cookies + four;
  cookies_total += four;
  let paragraphe = "Vous avez " + cookies.toString() + " cookies";
document.getElementById("nbcookies").innerHTML = paragraphe;
  let paragraphe4 = "Vous avez produit " + cookies_total.toString() + " cookies depuis le début de l'aventure";
document.getElementById("compteur").innerHTML = paragraphe4;
}
function cuire() {
  if (cookies >= 25) {
    cookies = cookies - 25;
    four = four + usines;
    let paragraphe = "Vous avez " + cookies.toString() + " cookies";
document.getElementById("nbcookies").innerHTML = paragraphe;
    console.log("hey2")
    let paragraphe2 = "Vous avez " + four.toString() + "      fours";
    document.getElementById("fours").innerHTML = paragraphe2;
  }
  else {
    alert("Tu n'a pas assé de cookies pour acheter un nouveau four");
  }
}
function construire() {
  if (cookies >= 500) {
    cookies -= 500;
    usines += 1;
    let paragraphe = "Vous avez " + cookies.toString() + " cookies";
    document.getElementById("nbcookies").innerHTML = paragraphe;
    let paragraphe3 = "Vous avez " + usines.toString() + " usines";
    document.getElementById("usines").innerHTML = paragraphe3;
  }
  else {
    alert("Tu n'a pas assé de cookies pour construire une nouvelle usine");
  }
}