import os
from PIL import Image

def decouper_tileset(chemin_image, dossier_sortie, taille_tuile, prefixe_poids="1"):
    """
    Découpe une image (tileset) en tuiles individuelles.
    
    :param chemin_image: Le chemin vers l'image source (ex: "planche_herbe.png")
    :param dossier_sortie: Le dossier où sauvegarder les tuiles (ex: "assets/map/plaine")
    :param taille_tuile: La taille d'une tuile en pixels (ex: 32 pour du 32x32)
    :param prefixe_poids: Le préfixe pour votre système de rareté (ex: "1" pour commun)
    """

    try:
        # 2. Ouvrir l'image source
        img = Image.open(chemin_image)
    except FileNotFoundError:
        print(f"❌ Erreur : L'image '{chemin_image}' est introuvable.")
        return

    largeur_img, hauteur_img = img.size

    # 3. Calculer combien de tuiles on peut extraire
    colonnes = largeur_img // taille_tuile
    lignes = hauteur_img // taille_tuile
    
    total_tuiles = colonnes * lignes
    print(f"✂️ Découpage de l'image {largeur_img}x{hauteur_img} en {total_tuiles} tuiles de {taille_tuile}x{taille_tuile}...")

    index = 60
    
    # 4. Boucle de découpage (de haut en bas, de gauche à droite)
    for y in range(lignes):
        for x in range(colonnes):
            # Calcul des coordonnées du rectangle à découper (gauche, haut, droite, bas)
            gauche = x * taille_tuile
            haut = y * taille_tuile
            droite = gauche + taille_tuile
            bas = haut + taille_tuile

            # Découpage de la zone
            tuile = img.crop((gauche, haut, droite, bas))
            
            # Formatage du nom : ex -> "1_tuile_0.png" (parfait pour votre AssetManager !)
            nom_fichier = f"{prefixe_poids}_tuile_{index}.png"
            chemin_sauvegarde = os.path.join(dossier_sortie, nom_fichier)
            
            # Sauvegarde de l'image découpée
            tuile.save(chemin_sauvegarde)
            index += 1

    print(f"✅ Terminé ! {index} tuiles ont été enregistrées dans '{dossier_sortie}'.")

# ==========================================
# ZONE DE TEST / UTILISATION
# ==========================================
if __name__ == "__main__":
    # Paramètres à modifier selon tes besoins
    IMAGE_SOURCE = "3.png" # L'image que tu as téléchargée
    DOSSIER_DESTINATION = "assets/map/foret" # Là où ça doit aller pour NeoRiza
    TAILLE_TUILE = 32 # La taille de tes carrés (ex: 32 ou 64)
    
    # On lance la fonction (avec un poids de "1" par défaut pour que ça soit commun)
    decouper_tileset(IMAGE_SOURCE, DOSSIER_DESTINATION, TAILLE_TUILE, prefixe_poids="1")
