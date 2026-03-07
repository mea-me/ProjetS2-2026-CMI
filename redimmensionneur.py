import os
from PIL import Image

def redimensionner_dossier(dossier_entree, dossier_sortie, nouvelle_taille):
    """
    Parcourt un dossier et redimensionne toutes les images en un format carré (ex: 16x16)
    avec un filtre de haute qualité pour éviter l'effet pixelisé.
    
    :param dossier_entree: Dossier contenant les images originales (ex: "assets/brut")
    :param dossier_sortie: Dossier où sauvegarder les images (ex: "assets/map/plaine")
    :param nouvelle_taille: La taille en pixels du carré final (ex: 16)
    """
    
    # 1. Sécurité : Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
        print(f"📁 Dossier de sortie créé : {dossier_sortie}")

    # 2. Lister les fichiers compatibles
    extensions_valides = (".png", ".jpg", ".jpeg")
    fichiers = [f for f in os.listdir(dossier_entree) if f.lower().endswith(extensions_valides)]
    
    if not fichiers:
        print(f"⚠️ Aucune image trouvée dans '{dossier_entree}'.")
        return

    print(f"⚙️ Redimensionnement de {len(fichiers)} images en {nouvelle_taille}x{nouvelle_taille}...")

    # 3. Traiter chaque image
    compteur = 0
    for nom_fichier in fichiers:
        chemin_entree = os.path.join(dossier_entree, nom_fichier)
        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
        
        try:
            with Image.open(chemin_entree) as img:
                # C'est ici que la magie opère pour le côté "joli" :
                # Image.Resampling.LANCZOS est le meilleur filtre pour réduire une image sans perte de qualité.
                img_reduite = img.resize((nouvelle_taille, nouvelle_taille), Image.Resampling.LANCZOS)
                
                # Sauvegarde en gardant la transparence si c'est un PNG
                img_reduite.save(chemin_sortie)
                compteur += 1
                
        except Exception as e:
            print(f"❌ Erreur lors du traitement de '{nom_fichier}' : {e}")

    print(f"✅ Terminé ! {compteur} images sauvegardées dans '{dossier_sortie}'.")


# ==========================================
# ZONE DE PARAMÉTRAGE
# ==========================================
if __name__ == "__main__":
    # Dossier où tu as mis tes images trop grandes
    DOSSIER_SOURCE = "assets/temp" 
    
    # Dossier où le script va ranger les images à la bonne taille
    DOSSIER_DESTINATION = "assets/map/foret" 
    
    # La taille cible (ex: 16 pour du 16x16, 32 pour du 32x32)
    TAILLE_CIBLE = 32
    
    redimensionner_dossier(DOSSIER_SOURCE, DOSSIER_DESTINATION, TAILLE_CIBLE)