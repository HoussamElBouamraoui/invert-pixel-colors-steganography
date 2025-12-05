from PIL import Image
import argparse

# Garde seulement les pixels proches des primaires (R,G,B) et du blanc; le reste devient noir.

def is_close(c, target, tol=15):
    return abs(c[0]-target[0]) <= tol and abs(c[1]-target[1]) <= tol and abs(c[2]-target[2]) <= tol

# Déchiffrement César: inverse avec clé positive (par défaut +1)
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filtrage et déchiffrement (César) optionnel')
    parser.add_argument('--input', default='challenge.png', help='Image d\'entrée (PNG)')
    parser.add_argument('--output', default='output_inverted.png', help='Image de sortie filtrée (PNG)')
    parser.add_argument('--ciphertext', default='', help='Texte chifré lu sur l\'image; si fourni, sera déchifré en César')
    parser.add_argument('--key', type=int, default=1, help='Clé César pour déchiffrement (par défaut +1)')
    args = parser.parse_args()

    img = Image.open(args.input).convert('RGB')

    keep_colors = [(255,0,0), (0,255,0), (0,0,255)]  # Rouge, Vert, Bleu
    out_pixels = []

    for (r, g, b) in img.getdata():
        c = (r, g, b)
        keep = False
        # Blanc proche
        if r >= 240 and g >= 240 and b >= 240:
            keep = True
        else:
            # Vérifier proximité des primaires
            for t in keep_colors:
                if is_close(c, t, tol=20):
                    keep = True
                    break
        out_pixels.append(c if keep else (0,0,0))

    out_img = Image.new('RGB', img.size)
    out_img.putdata(out_pixels)
    out_img.save(args.output, 'PNG')
    print(f'Image filtrée générée: {args.output}')

    # Déchiffrement optionnel
    if args.ciphertext:
        plaintext = caesar_decipher(args.ciphertext, key=args.key)
        print(f'Message déchiffré (César, clé=+{args.key}): {plaintext}')
