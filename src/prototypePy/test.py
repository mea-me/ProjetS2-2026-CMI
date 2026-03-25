def NouvelleEspecePointDInterrogation(popu):
    '''renvoie un agent si les conditions requises pour une nouvelle espece sont atteintes, None sinon
    arg : popu est la liste population mais ne contenant que des individus d'une meme espece'''
    for agent in popu:
        similaires = 0
        for agent_bis in popu:
            if agent != agent_bis and moyenne_des_differences(agent,agent_bis)<=0.2:
                similaires += 1
        differents = 0
        for agent_bis in popu:
            if agent != agent_bis and moyenne_des_differences(agent,agent_bis)>0.3:
                differents += 1

        if len(popu)>4 and similaires >= len(popu)/4 and differents >= len(popu)/2:
            return agent

    return None

def NouvelleEspecePointDInterrogation(popu):
    """!
    @brief Cherche si un individu a suffisamment muté pour fonder une nouvelle espèce.
    @param popu Liste contenant TOUS les individus d'une MÊME espèce.
    @return L'individu fondateur de la nouvelle espèce, ou None si pas de spéciation.
    """
    taille_pop = len(popu)
    if taille_pop < 5 : # pas besoin de réfléchir si y a pas assez d'indiv
        return None
    
    for agent in popu:
        similaires = 0
        differents = 0

        for agent_bis in popu:
            if agent != agent_bis : #pas de test avec soi mm
                distance = moyenne_des_differences(agent,agent_bis)

                if distance <= 0.2:
                    similaires += 1
                elif distance > 0.3:
                    differents += 1

        # si sous-groupe (similaires) + éloigné de la masse (différents)
        if similaires >= taille_pop/4 and differents >= taille_pop / 2:
            return agent

    return None