"""!
@file map_generation.py
@brief Module de gestion et de génération procédurale de l'environnement (WorldMap et Biomes).
"""

import os, pygame
from random import choices, gauss, randint, uniform

class AssetManager:
    """!
    @brief Charge et stocke les images des biomes en gérant les probabilités d'apparition.
    @param tile_size Taille des tile_size en pixels (a priori ça restera 16).
    """

    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.assets = {}  # Format: {"foret": {"images": [...], "poids": []}}
        self.load_all_assets()

    def load_all_assets(self):
        base_path = "assets/maps"

        # Poids associés aux préfixes des fichiers (1_, 2_, 3_)
        poids_prefixe = {"1": 0.70, "2": 0.25, "3": 0.05}

        for nom_biome in dico_biomes.keys():
            chemin = os.path.join(base_path, nom_biome)
            self.assets[nom_biome] = {"images": [], "poids": []}

            target_size = 32 if nom_biome == "foret" else self.tile_size

            for fichier in os.listdir(chemin):
                if fichier.endswith(".png"):
                    img = pygame.image.load( os.path.join(chemin, fichier) ).convert_alpha()
                    img = pygame.transform.scale(img, (target_size, target_size))
                    poids = poids_prefixe[fichier[0]]

                    self.assets[nom_biome]["images"].append(img)
                    self.assets[nom_biome]["poids"].append(poids)


# ----------------------------------------


class Biome:
    """!
    @brief Représente une zone rectangulaire (un biome) sur la carte.
    @details Contient les données géométriques et climatiques de la zone.
    """

    def __init__(self, nom, x, y, width, height):
        """!
        @brief Constructeur de la classe Biome.
        @param nom Nom du biome (doit exister dans dico_biomes).
        @param x Position X du coin supérieur gauche.
        @param y Position Y du coin supérieur gauche.
        @param width Largeur du biome.
        @param height Hauteur du biome.
        """
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        infos = dico_biomes[nom]
        self.température = infos["température"]
        self.humidité = infos["humidité"]
        self.color = infos["color"]

        self.rect = pygame.Rect(x, y, width, height)

    def draw_biome(self, surface, asset_manager):
        """!
        @brief Dessine le biome sur la surface donnée, avec textures si disponibles.
        @param surface Objet pygame.Surface sur lequel dessiner.
        @param asset_manager Le gestionnaire d'images (objet).
        """
        if self.nom != "foret":
            pygame.draw.rect(surface, self.color, self.rect)  # couleur de fond # couleur de fond

        if asset_manager and self.nom in asset_manager.assets:  # si y a des images
            data = asset_manager.assets[self.nom]  # "foret": {"images": [...], "poids": []}
            if data["images"]:  # pas une liste vide

                if not self.nom == "foret":
                    surface.set_clip(self.rect)  # pas déborder
                
                tile_size = asset_manager.tile_size
                step = tile_size
                if self.nom == "foret":
                    tile_size *= 2 

                # force alignement sur une même "grille" proportionnelle a tile_size (toubienaligné)
                start_x = (int(self.rect.left) // tile_size) * tile_size
                start_y = (int(self.rect.top) // tile_size) * tile_size

                # parcours par cases                     pas = tile_size
                
                for pX in range(start_x, self.rect.right, step):  #  →
                    for pY in range(start_y, self.rect.bottom, step):  #  ↓
                        # choix avec nos pondérations
                        img = choices(data["images"], weights=data["poids"])[0]
                        surface.blit(img, (pX, pY))  # on la place sur sa case

                surface.set_clip(None)  # pas oublier d'enlever le clipping pour les tiles suivantes

    def contains(self, x, y):
        """!
        @brief Vérifie si un point (x, y) se trouve à l'intérieur du biome.
        @param x Coordonnée X à tester.
        @param y Coordonnée Y à tester.
        @return True si le point est dans le biome, False sinon.
        """
        return self.rect.collidepoint(x, y)

    def get_pos(self):
        """!
        @brief Récupère la position d'origine du biome.
        @return Un tuple (x, y).
        """
        return (self.x, self.y)

    def __repr__(self):
        return f"{self.nom} [Pos: {self.x},{self.y}] (T={self.température}, H={self.humidité})"


# Format : "nom": {"température": T, "humidité": H, "color": (R, G, B)}
dico_biomes = {
    "ocean": {"température": 10, "humidité": 100, "color": (66, 172, 175)},
    "lagon": {"température": 12, "humidité": 100, "color": (119, 192, 180)},
    "plaine": {"température": 15, "humidité": 30, "color": (177, 211, 84)},
    "foret": {"température": 25, "humidité": 80, "color": (118, 202, 109)},
    "desert": {"température": 40, "humidité": 0, "color": (231, 213, 147)},
    "montagne": {"température": -5, "humidité": 20, "color": (128, 128, 128)},
    "neige": {"température": -20, "humidité": 60, "color": (247, 255, 255)},
}

class WorldMap:
    """!
    @brief Gestionnaire principal de la carte et de la génération procédurale.
    """

    def __init__(self, width, height):
        """!
        @brief Constructeur de la carte du monde.
        @param width Largeur totale de la carte (écran).
        @param height Hauteur totale de la carte (écran).
        @param biomes Liste des objets Biome.
        @param background_biome Biome de fond.
        @param merge_img Image de la map pré-calculée.
        """
        self.width = width
        self.height = height
        self.biomes = []
        self.background_biome = "ocean"
        self.merge_img = None
        self.asset_manager = AssetManager(tile_size=16)

    def add_zone(self, nom, x, y, width, height):
        """!
        @brief Instancie et ajoute un nouveau biome à la liste.
        """
        self.biomes.append(Biome(nom, x, y, width, height))

    def get_infos_at(self, x, y):
        """!
        @brief Récupère les données climatiques au point donné.
        @details Parcourt la liste à l'envers (logique de calques : le dernier ajouté est au-dessus).
        @param x Coordonnée X.
        @param y Coordonnée Y.
        @return Tuple (température, humidité, nom_biome).
        """
        for b in reversed(self.biomes):
            if b.contains(x, y):
                return b.température, b.humidité, b.nom

        bg = dico_biomes[self.background_biome]
        return bg["température"], bg["humidité"], self.background_biome


    def procedural_generation(self, taille=80, complx=3, composition=None, bg_biome="ocean"):
        """
        @brief Génère une carte complète avec continents, plages, et biomes internes.
        @param taille Nombre de base définissant le volume de l'ossature (continents).
        @param complx Facteur de complexité [1 à 5] modifiant la densité et l'éparpillement.
        """
        self.background_biome = bg_biome
        if composition is None:
            composition = {
                "foret": 5, 
                "desert": 5, 
                "neige": 5, 
                "montagne": 5
            }
        
        complx = max(1, min(int(complx), 5))
        complx *= 2

        ###### Gération de la couche terrestre de 1er niveau
        ossature = []

        for _ in range(taille):
            # génération aléatoire de son volume
            bW = uniform(0.05, 0.25) * self.width
            bH = uniform(0.05, 0.25) * self.height

            # gauss concentre les valeurs vers le centre
            bX = gauss(self.width / 2, self.width / 5) - bW / 2
            bY = gauss(self.height / 2, self.height / 5) - bH / 2

            ossature.append(Biome("plaine", bX, bY, bW, bH))

        ###### Création de la transition 
        if self.background_biome in ["ocean", "lagon"]:
            self._shallow_water_maker(ossature) # Dégradé d'eau
            self._beach_maker(ossature) # Plage
        else:
            # Si le fond n'est PAS aquatique : pas de plage ni dégradé
            for t in ossature:
                self.biomes.append(t)

        ###### Génération des biomes intra couche terrestre de 1er niveau
        reduc = complx**0.5 #réduire taille et forcer a se chevaucher -> anti-trous

        # calcule dynamique de intra_biomes
        intra_biomes = {}
        for nom, base_clusters, base_rects, tmin, tmax, spread in [
        ("foret", randint(1, complx), int(8 * complx**1.5), 0.04/reduc, 0.12/reduc, 0.12/reduc),
        ("desert", randint(1, complx), int(5 * complx**1.5), 0.08/reduc, 0.18/reduc, 0.08/reduc),
        ("neige", randint(1, complx), int(4 * complx**1.5), 0.03/reduc, 0.12/reduc, 0.07/reduc),
        ("montagne", randint(1, complx), int(taille * 0.15), 0.03, 0.08, 0.05)]:
            
            val_slider = composition[nom]

            # slider à 0 : on annule ce biome
            if val_slider == 0:
                continue
                
            # De 1 à 5: * normal (0.2 -> 1.0)
            # De 6 à 10: * quadratique (1 -> 4)
            multi_qte = (val_slider / 5.0) if val_slider <= 5 else ((val_slider / 5.0) ** 2)
            
            # La taille des zones grossit aussi 
            multi_taille = 0.5 + (val_slider / 10.0)

            intra_biomes[nom] = {
                "clusters": max(1, int(base_clusters * multi_qte)),
                "rects": max(1, int(base_rects * multi_qte)),
                "t_min": tmin * multi_taille,
                "t_max": tmax * multi_taille,
                "spread": spread * (multi_taille * 1.2), # L'étalement augmente encore plus
            }

        # mémoriser les épicentres --> éparpiller
        epicentres_utilises = []
        dist_x_min = 0.13 * self.width
        dist_y_min = 0.13 * self.height

        for nom_biome, cfg in intra_biomes.items():
            for _ in range(cfg["clusters"]):
                # choisir un épicentre pour la zone dans la map
                centreX = uniform(0.1, 0.9) * self.width
                centreY = uniform(0.1, 0.9) * self.height

                # s'éloigner des autres clusters (10 essais max)
                essais = 10
                trop_proche = True
                while trop_proche and essais > 0:
                    for (eX, eY) in epicentres_utilises:
                        # - de 20% d'un autre épicente
                        if (abs(centreX - eX) < dist_x_min and
                            abs(centreY - eY) < dist_y_min):
                            trop_proche = True
                            break 

                        else:
                            trop_proche = False

                    # sinon nouveau épicentre
                    centreX = uniform(0.1, 0.9) * self.width
                    centreY = uniform(0.1, 0.9) * self.height

                    essais -= 1

                # on add la position finale
                epicentres_utilises.append((centreX, centreY))
                
                noyau_W = None
                for _ in range(cfg["rects"]):
                    bX = gauss(centreX, cfg["spread"] * self.width)
                    bY = gauss(centreY, cfg["spread"] * self.height)

                    # terre ferme
                    _, _, nom_actuel = self.get_infos_at(bX, bY)

                    # montagnes = indépendantes --> pas besoin d'être sur la plaine
                    if nom_actuel == "plaine" or nom_biome == "montagne":
                        if noyau_W is None:
                            # ANTI-TROUS : gros bloc "noyau" au centre
                            noyau_W = cfg["t_max"] * self.width
                            noyau_H = cfg["t_max"] * self.height
                            self.add_zone( nom_biome, centreX - noyau_W / 2, centreY - noyau_H / 2, noyau_W, noyau_H )

                        bW = uniform(cfg["t_min"], cfg["t_max"]) * self.width
                        bH = bW * uniform(0.6, 1.4)  # pas de carrés parfaits

                        self.add_zone(nom_biome, bX - bW / 2, bY - bH / 2, bW, bH)

        self.map_merge()

    def _shallow_water_maker(self, ossature):
        """!
        @brief Génère une sous-couche d'eau claire pour faire un dégradé topologique.
        """
        epaisseur = 0.02 * self.width  # 2% de l'écran, plus large que la plage
        for t in ossature:
            pX, pY = t.x - epaisseur, t.y - epaisseur
            pW, pH = t.width + (epaisseur * 2), t.height + (epaisseur * 2)
            self.add_zone("lagon", pX, pY, pW, pH)

    def _beach_maker(self, ossature):
        """!
        @brief Génère une couche de sable aux extrémités des continent.
        """
        epaisseur = 0.008 * self.width
        for t in ossature:
            pX, pY = t.x - epaisseur, t.y - epaisseur
            pW, pH = t.width + (epaisseur * 2), t.height + (epaisseur * 2)
            self.add_zone("desert", pX, pY, pW, pH)

        for t in ossature: # remettre la terre par dessus
            self.biomes.append(t)

    def map_merge(self):
        """!
        @brief Pré-calcule le rendu de la carte sur une surface unique
        @details Élimine le goulot d'étranglement des appels de dessin multiples par frame.
        """
        self.merge_img = pygame.Surface((self.width, self.height))

        bg_color = dico_biomes[self.background_biome]["color"]
        self.merge_img.fill(bg_color)

        # tiles de fond
        if self.background_biome in self.asset_manager.assets and self.asset_manager.assets[self.background_biome]["images"]:
            data = self.asset_manager.assets[self.background_biome]
            tile_size = self.asset_manager.tile_size
            
            # éviter de dessiner des tiles sous la carte si taille d'écran géante (opti)
            for px in range(0, self.width, tile_size):
                for py in range(0, self.height, tile_size):
                    img = choices(data["images"], weights=data["poids"])[0]
                    self.merge_img.blit(img, (px, py))

        # PAR DESSUS, le reste du monde
        for b in self.biomes:
            b.draw_biome(self.merge_img, self.asset_manager)

    def paint(self, surface):
        """!
        @brief Affiche la carte pré-calculée sur l'écran.
        @param surface Pygame surface principale (l'écran).
        """
        if not self.merge_img:
            self.map_merge()

        surface.blit(self.merge_img, (0, 0))
