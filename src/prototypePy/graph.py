import json
import matplotlib.pyplot as plt
import seaborn as sns

# Appliquer le style Seaborn
sns.set_theme(style="darkgrid")

def save_json(liste_especes, suivi_espece):
    data_export = {}
    for esp in liste_especes:
        # JSON pref les clés texte
        str_id = str(esp.id_espece)
        infos = suivi_espece[esp.id_espece]
        
        data_export[str_id] = {
            "parent": infos[0],
            "annee_naissance": infos[1],
            "annee_mort": infos[2],
            "historique_effectif": esp.effectif
        }
    
    with open("./data/evolution_data.json", "w") as f:
        json.dump(data_export, f, indent=4)

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
    plt.xlim(0, max_annee) 
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
    plt.tight_layout() # ajuster les marges
    
    plt.show()
