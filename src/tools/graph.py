import json
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from src.simulation.environnement.map_generation import dico_biomes

# Appliquer le style Seaborn
sns.set_theme(style="darkgrid")

def normaliser_serie(y, longueur):
    # si valeur unique
    if not isinstance(y, list):
        return [y] * longueur

    # si liste trop courte
    if len(y) < longueur:
        return y + [y[-1]] * (longueur - len(y))

    return y

def save_json(liste_especes, suivi_espece):
    data_export = {}
    for esp in liste_especes:     
        a_existe = max(esp.effectif) > 0 if esp.effectif else False
        # JSON pref les clés texte
        str_id = str(esp.id_espece)
        infos = suivi_espece[esp.id_espece]
        
        
        data_export[str_id] = {
            "parent": infos[0],
            "annee_naissance": infos[1],
            "annee_mort": infos[2],
            "historique_effectif": esp.effectif,
            "a_existe" : a_existe,
            "allele": esp.dico_evolution_alleles
        }
    
    with open("././data/evolution_data.json", "w") as f:
        json.dump(data_export, f, indent=4)

def generer_graphique_allele(allele, age):
    with open("././data/evolution_data.json", "r") as f:
        data = json.load(f)

    plt.figure(figsize=(12, 6))
    max_annee = 0 #pour regler le x

    if allele == "humidité" or allele == "température":
        l = list(range(age))
        for biome in dico_biomes.keys():
            vals = dico_biomes[biome][allele]
            vals = normaliser_serie(vals, age)

            sns.lineplot(
                x=l,
                y=vals,
                label=f"{allele} dans {biome}",
                linewidth=3
            )

    for esp_id, infos in data.items():
        # Si l'espèce n'a pas d'historique, on l'ignore
        if infos["a_existe"]:
            historique_brut = infos["allele"][allele]

            annees_vecues = len(historique_brut) if isinstance(historique_brut, list) else 1
            annee_naissance = infos["annee_naissance"] // 60

            annees_x = list(range(annee_naissance, annee_naissance + annees_vecues))
            historique = normaliser_serie(historique_brut, annees_vecues)

            #maj anne max
            if annees_x[-1] > max_annee:
                max_annee = annees_x[-1]
                
            label = f"Espèce {esp_id}"
            if infos["annee_mort"] is not None:
                label += f" (Éteinte en {infos['annee_mort']//60})"
                
            sns.lineplot(
                x=annees_x,
                y=historique,
                label=label,
                linewidth=2
            )

    plt.title(f"Évolution de l'allèle {allele} des espèces au fil du temps", fontsize=16)
    plt.xlabel("Années", fontsize=12)
    plt.ylabel("Valeur", fontsize=12)
    if max_annee > 0:
        plt.xlim(0, max_annee)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
    plt.tight_layout() # ajuster les marges
    
    plt.show()

def generer_graphique_population():
    with open("././data/evolution_data.json", "r") as f:
        data = json.load(f)

    plt.figure(figsize=(12, 6))
    max_annee = 0 #pour regler le x

    for esp_id, infos in data.items():
        # Si l'espèce n'a pas d'historique, on l'ignore
        if infos["a_existe"]:
            historique = infos["historique_effectif"]
            annee_naissance = infos["annee_naissance"] // 60

            annees_vecues = len(historique)
            annees_x = list(range(annee_naissance, annee_naissance + annees_vecues))
            
            if annees_x[-1] > max_annee:
                max_annee = annees_x[-1]
                
            label = f"Espèce {esp_id}"
            if infos["annee_mort"] is not None:
                label += f" (Éteinte en {infos['annee_mort']//60})"
            
            sns.lineplot(x=annees_x, y=historique, label=label, linewidth=2)

    plt.title("Évolution de la population des espèces au fil du temps", fontsize=16)
    plt.xlabel("Années", fontsize=12)
    plt.ylabel("Effectifs", fontsize=12)
    if max_annee > 0:
        plt.xlim(0, max_annee)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
    plt.tight_layout() # ajuster les marges
    
    plt.show()

def generer_arbre_genealogique():
    with open("././data/evolution_data.json", "r") as f:
        data = json.load(f)

    G = nx.DiGraph()

    for esp_id, infos in data.items():
        if infos["a_existe"] : # vérification de si l'espece a existé
            G.add_node(esp_id)
            parent_id = infos.get("parent")
            if parent_id is not None:
                parent_id_str = str(parent_id)
                if parent_id_str in data and parent_id_str != esp_id:
                    G.add_edge(parent_id_str, esp_id)

    generations = {}
    
    def calculer_generation(noeud):
        if noeud in generations:
            return generations[noeud]
        parent = data[noeud].get("parent")
        if parent is None :
            generations[noeud] = 0
            return 0
        gen = calculer_generation(str(parent)) + 1
        generations[noeud] = gen
        return gen

    for noeud in G.nodes():
        G.nodes[noeud]['layer'] = calculer_generation(noeud)

    pos_initiales = nx.multipartite_layout(G, subset_key="layer", align="vertical")
    
    pos_verticales = {noeud: (x, -y) for noeud, (y, x) in pos_initiales.items()}

    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.set_title("Arbre d'évolution des espèces", fontsize=16, pad=20)

    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    cmap = plt.cm.plasma

    # fait le graphe fr
    nx.draw(G, pos_verticales, 
            ax=ax,
            with_labels=True, 
            node_size=2000, 
            node_color="indigo", 
            font_size=10, 
            font_weight="bold", 
            font_color="white", 
            edge_color=edge_colors, 
            edge_cmap=cmap,
            arrows=True, 
            arrowstyle="->",
            arrowsize=10, 
            width=2)

    plt.tight_layout()
    plt.show()

def generer_dashboard_graphes(age):
    with open("././data/evolution_data.json", "r") as f:
        data = json.load(f)

    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("Vue globale de l'évolution", fontsize=18)

    # ================= POPULATION =================
    ax = axs[0, 0]
    for esp_id, infos in data.items():
        if infos["a_existe"]:
            histo = infos["historique_effectif"]
            naissance = infos["annee_naissance"] // 60

            x = list(range(naissance, naissance + len(histo)))
            ax.plot(x, histo, label=f"E{esp_id}")

    ax.set_title("Population")
    ax.set_ylabel("Effectif")

    # ================= TEMPÉRATURE =================
    ax = axs[0, 1]
    for biome in dico_biomes:
        vals = normaliser_serie(dico_biomes[biome]["température"], age)
        ax.plot(range(age), vals, label=biome)

    ax.set_title("Température par biome")

    # ================= HUMIDITÉ =================
    ax = axs[1, 0]
    for biome in dico_biomes:
        vals = normaliser_serie(dico_biomes[biome]["humidité"], age)
        ax.plot(range(age), vals, label=biome)

    ax.set_title("Humidité par biome")
    ax.set_xlabel("Années")

    # ================= ALÈLE EXEMPLE =================
    ax = axs[1, 1]
    allele = "taille"  # exemple
    for esp_id, infos in data.items():
        if infos["a_existe"] and allele in infos["allele"]:
            histo_brut = infos["allele"][allele]
            longueur = len(histo_brut) if isinstance(histo_brut, list) else 1
            naissance = infos["annee_naissance"] // 60

            x = list(range(naissance, naissance + longueur))
            histo = normaliser_serie(histo_brut, longueur)

            ax.plot(x, histo, label=f"E{esp_id}")

    ax.set_title(f"Allèle : {allele}")
    ax.set_xlabel("Années")
    
    for ax in axs.flat:
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.show()