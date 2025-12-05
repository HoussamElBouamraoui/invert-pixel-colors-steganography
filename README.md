# Guide pratique — Mini-projet de stéganographie (Challenge + Solving)

Ce guide explique le principe utilisé, les scripts clés (`script.py` et `solving.py`), et les étapes pour générer l'image Challenge, la révéler, puis déchiffrer le message en César.

## 1) Principe

- On génère une image de bruit aléatoire (RGB) et on y écrit un texte par un masque en couleurs primaires (Rouge/Vert/Bleu) avec un léger jitter.
- Avant d'écrire le texte, on applique un chiffrement de César avec la clé −1, ce qui décale chaque lettre d'un cran vers la gauche.
- Pour révéler le texte, on applique un filtre couleur qui garde uniquement les pixels proches des primaires (et du blanc). Le texte apparait alors lisible mais encore chifré.
- Pour afficher le vrai message, on utilise le solving avec déchiffrement César inverse (clé +1).

## 2) Scripts et code clés

### `script.py` — Génération du Challenge

- Paramètres principaux:
  - `width`, `height`: dimensions de l'image
  - `message`: texte à camoufler (sera chifré par César −1)
  - `font_size`, `repeat`, `start_xy`, `line_spacing`: mise en page du texte
- Chiffrement de César:
  - Fonction `caesar_cipher(text, key)`
  - Applique la clé `-1` au message avant de dessiner
- Sortie: `challenge.png`

Extrait (logique clé):
```python
# --- Ajout: chiffrement de César avec clé = -1 ---
def caesar_cipher(text: str, key: int) -> str:
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            base = ord('A')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        elif 'a' <= ch <= 'z':
            base = ord('a')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        else:
            out.append(ch)
    return ''.join(out)

# Appliquer la clé -1
message = caesar_cipher(message, -1)
```

### `solving.py` — Révélation et déchiffrement

- Filtrage:
  - Conserve les pixels proches des couleurs primaires (R,G,B) et du blanc; les autres deviennent noirs.
  - Sortie: `output_inverted.png`
- Déchiffrement César:
  - Fonction `caesar_decipher(text, key=1)` avec clé +1 par défaut
  - Argument `--ciphertext` pour passer le texte chifré lu sur l'image filtrée
  - Affiche le "Message déchiffré (César, clé=+1)"

Extrait (logique clé):
```python
def caesar_decipher(text: str, key: int = 1) -> str:
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            base = ord('A')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        elif 'a' <= ch <= 'z':
            base = ord('a')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        else:
            out.append(ch)
    return ''.join(out)
```

## 3) Prérequis

- Python 3.8+
- Pillow (PIL)

Installation:
```powershell
python -m pip install --upgrade pip
pip install pillow
```

## 4) Étapes — Comment faire

1) Générer l'image Challenge
```powershell
python .\script.py
```
- Produit `challenge.png` avec le message chifré (César −1) camouflé sur bruit.

2) Révéler visuellement le texte par filtrage
```powershell
python .\solving.py --input .\challenge.png --output .\output_inverted.png
```
- Produit `output_inverted.png`, où le texte chifré est lisible.

3) Afficher le vrai message (déchiffrement César +1)
- Lisez le texte chifré visible dans `output_inverted.png`.
- Passez-le au solving:
```powershell
python .\solving.py --ciphertext "<votre_texte_chifre>" --key 1
```
- Exemple (de votre session):
```powershell
python .\solving.py --ciphertext "bxadq zskzr hr sgd adrs" --key 1
```
- Affiche:
```
Image filtrée générée: output_inverted.png
Message déchiffré (César, clé=+1): cyber atlas is the best
```

## 5) Conseils et limites

- Le mode visible est pédagogique mais facilement révélable par filtres.
- Si vous souhaitez un message totalement invisible visuellement, envisagez la stéganographie LSB (bits de poids faible) au lieu des couleurs primaires.
- Évitez la compression JPEG pour préserver les couleurs exactes.
- Si `arial.ttf` n'est pas disponible, Pillow utilisera une police par défaut; adaptez `font_size` si besoin.

## 6) Dépannage

- Si `challenge.png` n'apparaît pas, vérifiez les droits d'écriture et le répertoire courant.
- Si le texte filtré est peu lisible, augmentez `font_size` ou `repeat`, ou ajustez `line_spacing` dans `script.py`.
- Si le déchiffrement ne donne pas un sens, assurez-vous que la clé −1 a été utilisée dans `script.py` et que vous utilisez bien la clé +1 dans `solving.py`.

---

Ce guide couvre le flux simple Challenge → Filtrage → Déchiffrement César, avec commandes Windows PowerShell prêtes à copier.

