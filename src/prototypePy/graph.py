import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main import suivi_espece, liste_especes

sns.set_theme(style="darkgrid")

eff_total = []
for i in range(len(liste_especes)) : # listes des objects especes
    eff_total.append(liste_especes[i].effectif) # liste des evolutions d'effectifs de l'espece

data_espece = pd.DataFrame(liste_especes[0].effectif)
sns.scatterplot(x="nombre d'individus", y="année", data=data_espece)