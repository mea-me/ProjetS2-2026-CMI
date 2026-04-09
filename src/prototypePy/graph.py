import json
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Appliquer le style Seaborn
sns.set_theme(style="darkgrid")

def save_json(liste_especes, suivi_espece):
    data_export = {}
    for esp in liste_especes:
        s = 0
        for i in esp.effectif :
            s += i
        if s != 0:
            # JSON pref les clés texte
            str_id = str(esp.id_espece)
            infos = suivi_espece[esp.id_espece]
            
            data_export[str_id] = {
                "parent": infos[0],
                "annee_naissance": infos[1],
                "annee_mort": infos[2],
                "historique_effectif": esp.effectif,
                "allele": esp.dico_evolution_alleles
            }
    
    with open("./data/evolution_data.json", "w") as f:
        json.dump(data_export, f, indent=4)

def generer_graphique_allele(allele):
    with open("./data/evolution_data.json", "r") as f:
        data = json.load(f)

    plt.figure(figsize=(12, 6))
    max_annee = 0 #pour regler le x

    for esp_id, infos in data.items():
        historique = infos["allele"][allele]
        annee_naissance = infos["annee_naissance"]//60
        
        # Si l'espèce n'a pas d'historique, on l'ignore
        if not historique:
            continue
            
        # axe de x pour cette espece
        annees_vecues = len(historique)
        annees_x = list(range(annee_naissance, annee_naissance + annees_vecues))
        
        #maj anne max
        if annees_x[-1] > max_annee:
            max_annee = annees_x[-1]
            
        label = f"Espèce {esp_id}"
        if infos["annee_mort"] is not None:
            label += f" (Éteinte en {infos['annee_mort']//60})"
            
        sns.lineplot(x=annees_x, y=historique, label=label, linewidth=2)

    
    plt.title(f"Évolution de l'allèle {allele} des espèces au fil du temps", fontsize=16)
    plt.xlabel("Années", fontsize=12)
    plt.ylabel("Valeur", fontsize=12)
    if max_annee > 0:
        plt.xlim(0, max_annee)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
    plt.tight_layout() # ajuster les marges
    
    plt.show()

def generer_graphique_population():
    with open("./data/evolution_data.json", "r") as f:
        data = json.load(f)

    plt.figure(figsize=(12, 6))
    max_annee = 0 #pour regler le x

    for esp_id, infos in data.items():
        historique = infos["historique_effectif"]
        annee_naissance = infos["annee_naissance"]//60
        
        # Si l'espèce n'a pas d'historique, on l'ignore
        if not historique:
            continue
            
        # axe de x pour cette espece
        annees_vecues = len(historique)
        annees_x = list(range(annee_naissance, annee_naissance + annees_vecues))
        
        #maj anne max
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
    with open("./data/evolution_data.json", "r") as f:
        data = json.load(f)

    G = nx.DiGraph()

    for esp_id, infos in data.items():
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
    #plt.gcf().set_facecolor('#1e1e1e') # fond de la fenêtre
    ax = plt.gca()
    #ax.set_facecolor('#1e1e1e')        # fond du graphique"""

    plt.title("Arbre d'évolution des espèces", fontsize=16, color="white", pad=20)

    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
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