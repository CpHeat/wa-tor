# Wa-Tor Simulation
Ce projet est une simulation du monde marin inspirée du modèle Wa-Tor, où des poissons et des requins évoluent, se déplacent, se reproduisent, et interagissent sur une grille torique.

## 📂 Structure des classes

                    ┌────────────────┐
                    │    Animal      │  
                    └────────────────┘
                       ▲    |      ▲
              ┌─────────┘   |       └─────────┐
      ┌─────────────┐       |          ┌─────────────┐
      │    Fish     │       |          │    Shark    │
      └─────────────┘       |          └─────────────┘
                            | 
                    ┌────────────────┐                      ┌────────────────────────────┐
                    │    Planet      │----------------------│    SimulationControl      │
                    └────────────────┘                      └────────────────────────────┘



---

### **Animal** (`animal.py`)

- Classe abstraite.
- Attributs :
  - `x`, `y` (coordonnées sur la grille)
  - `age`, `reproduction_time`, `reproduction_left`
- Méthodes :
  - `choice_direction()` → choisit une direction au hasard en tenant compte des bords.
  - `reproduce()` → détermine si l’animal peut se reproduire.

---

### **Fish** (`classes/fish.py`)

- Hérite de `Animal`.
- Comporte un comportement simple : bouger et se reproduire.
- Méthode clé attendue :
  - `move()` → choisit le déplacement vers une case libre.

---

### **Shark** (`classes/shark.py`)

- Hérite de `Animal`.
- Peut :
  - chasser et manger les poissons (`eat()`),
  - se déplacer (`move()`),
  - mourir de faim s’il ne mange pas (`starved_shark()` dans `Planet`).


---

### **Planet** (`planet.py`)

- Gère :
  - la grille torique,
  - le placement initial (`populate()`),
  - les déplacements et interactions des entités (`check_entities()`),
  - les statistiques (nombre de poissons, requins, morts, reproductions).


---

### **settings.py**

- Contient le dictionnaire `simulation_parameters` avec :
  - dimensions de la grille,
  - populations initiales,
  - options pour suivre/mélanger les entités.

---
### **SimulationControl** (`simulation_control.py`)

- Sert d’interface entre la logique de simulation (`Planet`) et l’interface graphique.  
- Rôles :
  - Lire les paramètres depuis l’interface utilisateur (`set_parameters()`).
  - Lancer la simulation (`start_simulation()`).
  - Gérer chaque étape temporelle (appelée “chronon”) (`simulation_step()`).
  - Mettre en pause ou reprendre (`pause_simulation()`).
  - Arrêter et réinitialiser (`stop_simulation()`).
- Utilise la classe `DataHandler` pour enregistrer les données à chaque étape.
- Dépend fortement d’un objet `interface` qui contient les composants graphiques : canevas, compteurs, boutons, etc.


## 🚀 Démarrer la simulation

1. **Installer Python 3 et les dépendances (si nécessaire dans le fichier requirements.txt)**

2. **Configurer les paramètres**  
Dans le fichier `settings.py` :
```python
simulation_parameters = {
    'grid_height': 20,
    'grid_width': 20,
    'fish_starting_population': 50,
    'shark_starting_population': 20,
    'follow_entities': True,
    'shuffle_entities': True
}
```
3. **Exécuter la simulation**
Assurez-vous d’avoir un fichier principal comme :
`python main.py`


## ⚙️ Fonctionnalités clés

✅ Déplacement aléatoire des animaux (nord, sud, est, ouest, avec rebouclage sur les bords)  
✅ Reproduction selon un cycle propre à chaque espèce  
✅ Prédation : les requins mangent les poissons  
✅ Statistiques : comptage des naissances, morts, entités restantes  
✅ Option de suivre des entités spécifiques (`follow_entities`)  
✅ Option de mélanger l’ordre des entités à chaque tour (`shuffle_entities`)  


