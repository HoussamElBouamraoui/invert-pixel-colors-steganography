from PIL import Image, ImageDraw, ImageFont
import random

# Paramètres
width, height = 800, 600
message = "cyber atlas is the best"  # message court pour visibilité comme l'exemple
font_size = 28
repeat = 5
start_xy = (320, 120)
line_spacing = 34

# --- Ajout: chiffrement de César avec clé = -1 ---
def caesar_cipher(text: str, key: int) -> str:
    out = []
    for ch in text:
        # Majuscules A-Z
        if 'A' <= ch <= 'Z':
            base = ord('A')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        # Minuscules a-z
        elif 'a' <= ch <= 'z':
            base = ord('a')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        else:
            # caractères non alphabétiques inchangés
            out.append(ch)
    return ''.join(out)

# Appliquer la clé -1
message = caesar_cipher(message, -1)

# 1. Créer une image de bruit aléatoire (fond)
noise_img = Image.new("RGB", (width, height))
pixels = noise_img.load()
for x in range(width):
    for y in range(height):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        pixels[x, y] = (r, g, b)

# 2. Créer un masque pour le message
mask = Image.new("1", (width, height), 0)
draw = ImageDraw.Draw(mask)
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

x0, y0 = start_xy
for i in range(repeat):
    draw.text((x0, y0 + i * line_spacing), message, font=font, fill=1)

# 3. Dessiner le message dans l'image originale avec des couleurs primaires
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Rouge, Vert, Bleu
for x in range(width):
    for y in range(height):
        if mask.getpixel((x, y)) == 1:
            color_idx = (x + y) % len(colors)
            r, g, b = colors[color_idx]
            # Camouflage léger par jitter
            r = max(0, min(255, r + random.randint(-8, 8)))
            g = max(0, min(255, g + random.randint(-8, 8)))
            b = max(0, min(255, b + random.randint(-8, 8)))
            pixels[x, y] = (r, g, b)

# 4. Sauvegarder le challenge
noise_img.save("challenge.png")