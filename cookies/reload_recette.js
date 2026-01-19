function calcul(x) {
  var peoples = document.getElementById("personnes").value;
  var y = x / 12 * peoples
  var y = Math.round(y)
  if (y < 1) {
    y += 1
  }
  return y
}
function reload_recette() {
  let paragraphe = calcul(2) + " oeufs, " + calcul(170) + " g de sucre, " + calcul(17) + "g de beurre doux, " + calcul(300) + "g de farine, " + calcul(200) + "g de pépites de chocolat, " + calcul(2) + " sachet de sucre vanillé, " + calcul(2) + " cuillére(s) a café de levure chimique et " + calcul(1) + " cuillére à café de sel (un peu de vanille).";
  document.getElementById("texte").innerHTML = paragraphe;
}