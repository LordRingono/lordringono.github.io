# Contrôle du site — autotests histologiques

Résultat : **PASS**.

Fichier testé : `/workspace/scratch/f3cb3bb97377/output/site/index.html`.

Empreinte SHA256 : `37ba5f8d7d320ad773b47caa1b8cf6459cd2898cfbc81cf9adbdc99d6b1e33a2`.

- 128 QCM ciblés dans neuf banques.
- 18 couples banque/profil vérifiés avec une clé donnant 20/20.
- 640 états de carte vérifiés : sujet avant correction ; sujet et corrigé après correction.
- 18 couples banque/profil vérifiés après fermeture logique et rechargement de l’application.
- 208 banques hors périmètre inchangées (2678 QCM).
- 3208 anciens fichiers conservés à l’identique, dont 172 fichiers d’audit.

## Méthode

Le JavaScript réel du site est exécuté avec le dom_adapter.cjs livré dans V4. Les réponses passent par le gestionnaire réel de changement des cases ; les fonctions réelles de correction, de rendu et de sauvegarde sont exécutées. Les copies de sources sont contrôlées dans le HTML produit pour chaque carte, y compris les QCM encore vides après une correction sélective partielle.

Les deux profils ont des réponses différentes, puis un nouvel environnement recharge leurs sauvegardes. TC3 Q17 est contrôlé avec une case « aucune proposition » explicitement choisie, distincte d’un QCM laissé vide. Le nouvel autotech ID 13 est contrôlé avec les lettres F–J et la clé GIJ.

## Portée

Le script et les chaînes HTML réels sont exécutés avec l’adaptateur DOM V4. Ce contrôle ne mesure pas le rendu graphique ou les pixels d’un navigateur.
