import pygame
from .genome import Genome
from random import choice, randint
from .allele import Allele, dico_alleles
from .individu import Individu
from .optimisation import QuadTree
from .environnement import WorldMap
from .__init__ import W, H, ALLOWED_MASK

class Livings:
    def __init__(self):
        self.populations = []

    def add_individu(self, individu):
        self.populations.append(individu)

    def score_survie(self, individu, world):
        température = individu.genome.get_val("température")
        humidité = individu.genome.get_val("humidité")
        adaptabilité = individu.genome.get_val("adaptabilité")
        agilité = individu.genome.get_val("agilité")
        age = individu.age
        env = world.get_infos_at(individu.rect.x, individu.rect.y)
        température_env = env[0]
        humidité_env = env[1]

        temp = abs(température - température_env)
        humi = abs(humidité - humidité_env)
        score = (age/600*(adaptabilité + 0.5*agilité))+(adaptabilité + 0.5*agilité) - (temp + humi)
        return score
    
    def predation(self, ind1, ind2, world):
        pred1 = ind1.genome.get_val("aggréssivité")
        pred2 = ind2.genome.get_val("aggréssivité")

        if abs(pred1 - pred2) >= 10:
            if pred1 > pred2 :
                if self.score_survie(ind1, world) > self.score_survie(ind2, world)-5:
                    masse = 0.6 * ind2.genome.get_val("masse")
                    self.kill(ind2)
                    if ind1.genome.get_val("régime") != "herbivore":
                        ind1.energie += masse
                elif randint(0, 100) < 50:
                    masse = 0.3 * ind2.genome.get_val("masse")
                    self.kill(ind2)
                    if ind1.genome.get_val("régime") != "herbivore":
                        ind1.energie += masse
            elif pred1 < pred2 :
                if self.score_survie(ind1, world) < self.score_survie(ind2, world)-5:
                    masse = 0.6 * ind1.genome.get_val("masse")
                    self.kill(ind1)
                    if ind2.genome.get_val("régime") != "herbivore":
                        ind2.energie += masse
                elif randint(0, 100) < 50:
                    masse = 0.3 * ind1.genome.get_val("masse")
                    self.kill(ind1)
                    if ind2.genome.get_val("régime") != "herbivore":
                        ind2.energie += masse
        else:
            if pred1 > pred2 :
                ind1.energie -= 5
                ind2.energie -= 10
            elif pred1 < pred2 :
                ind1.energie -= 10
                ind2.energie -= 5
                

    def reproduction(self, individu1, individu2, world):
        new_genome = Genome()
    
        # --- Génération du génome de l'enfant ---
        for allele1, allele2 in zip(individu1.genome.alleles, individu2.genome.alleles):
            if allele1.type in ('str', 'list'):
                parent_allele = choice([allele1, allele2])
                if isinstance(parent_allele.valeur, list):
                    valeur = parent_allele.valeur.copy()
                else:
                    valeur = parent_allele.valeur
                new_allele = Allele(
                    parent_allele.nom,
                    parent_allele.al_type,
                    parent_allele.req,
                    valeur,
                    parent_allele.mutation_rate,
                    parent_allele.mutation_step,
                    parent_allele.type
                )
            elif allele1.type == 'int':
                gosse_value = (allele1.valeur + allele2.valeur) // 2
                parent_allele = choice([allele1, allele2])
                new_allele = Allele(
                    parent_allele.nom,
                    parent_allele.al_type,
                    parent_allele.req,
                    gosse_value,
                    parent_allele.mutation_rate,
                    parent_allele.mutation_step,
                    parent_allele.type
                )
            new_genome.add_allele(new_allele)
        # --- Position du bébé ---
        x = (individu1.rect.x + individu2.rect.x) // 2
        y = (individu1.rect.y + individu2.rect.y) // 2
        # --- CRÉATION DU BÉBÉ AVEC LA CLASSE DU PREMIER IND ---
        # Si le parent est une espèce dérivée (Licorne, Blob, etc.)
        if individu1.__class__ is not Individu:
            bébé = individu1.__class__(x, y)
        # Si le parent est un Individu normal(random)
        else:
            bébé = Individu(x, y, individu1.id_espece)
        # --- Application du génome ---
        bébé.give_genome(new_genome.clone())
        bébé.give_rect(bébé.genome.get_val("taille"))
        bébé.genome.muter()
        # --- Ajout à la population ---
        self.populations.append(bébé)
        # --- Mort environnementale(PAS FINI) --- 
        temp = bébé.genome.get_val("température")
        hum = bébé.genome.get_val("humidité")
        env = world.get_infos_at(bébé.rect.x, bébé.rect.y)
        if abs(env[0] - temp) >= 20:
            if randint(0, 100) < 30:
                self.kill(bébé)
        elif abs(env[0] - temp) >= 10:
            if randint(0, 100) < 20:
                self.kill(bébé)
        elif abs(env[0] - temp) >= 5:
            if randint(0, 100) < 10:
                self.kill(bébé)
        
    def on_collision(self, ind1, ind2, world):
        env1 = world.get_infos_at(ind1.rect.x, ind1.rect.y)
        env2 = world.get_infos_at(ind2.rect.x, ind2.rect.y)
        temp1 = ind1.genome.get_val("température")
        temp2 = ind2.genome.get_val("température")

        if ind1.id_espece == ind2.id_espece:
            if ind1.age >= 60 and ind2.age >= 60 and ind1.age <= 600 and ind2.age <= 600:
                if abs(env1[0]-temp1) < 5 and abs(env2[0]-temp2) < 5:
                    self.reproduction(ind1, ind2, world)
                elif abs(env1[0]-temp1) <= 10 and abs(env2[0]-temp2) <= 10:
                    if randint(0,100) <= 75:
                        self.reproduction(ind1, ind2, world)
                else:
                    if randint(0,100) <= 20:
                        self.reproduction(ind1, ind2, world)
        
        else:
            self.predation(ind1, ind2, world)

    def update(self, screen_width, screen_height, world):
        quad = QuadTree(0, pygame.Rect(0, 0, screen_width, screen_height))
        quad.clear() 

        for ind in self.populations:
            quad.insert(ind)
            ind.update()
            if not ind.is_alive():
                self.kill(ind)
            elif self.score_survie(ind, world)<-32:
                ind.energie -= 10
            if ind.collision_cooldown > 0: 
                ind.collision_cooldown -= 1/60
            self.apply_boids(ind, quad)

            

        # déplacement Boids
        #self.handle_déplacement(quad, world)

        # collisions / reproduction
        self.handle_collisions(quad, world)

    # ---------- BOIDS ----------

    def get_neighbors(self, ind, quad):
        perception = ind.genome.get_val("perception")  # distance de vision
        zone = pygame.Rect(
            ind.rect.x - perception,
            ind.rect.y - perception,
            perception*2,
            perception*2
        )
        candidats = quad.retrieve(zone)
        #Filtre : même espèce uniquement
        voisins = [
            o for o in candidats
            if o is not ind and o.id_espece == ind.id_espece
        ]
        return voisins

    def rule_separation(self, ind, neighbors):
        taille = ind.genome.get_val("taille")
        agressivite = ind.genome.get_val("aggréssivité")
        min_dist = taille * 1.0  # distance de confort
        force_x = 0
        force_y = 0
        count = 0

        for other in neighbors:
            dx = ind.rect.x - other.rect.x
            dy = ind.rect.y - other.rect.y
            dist2 = dx*dx + dy*dy
            if dist2 == 0:
                continue
            dist = dist2**0.5

            # trop proche → on repousse
            if dist < min_dist * 0.5:  # on laisse une petite marge pour le contact
                force_x += dx / dist
                force_y += dy / dist
                count += 1

        if count > 0:
            force_x /= count
            force_y /= count

            # agressivité augmente la force de séparation
            coef = 0.02 + agressivite / 2000  # 0.02 à ~0.06
            force_x *= coef
            force_y *= coef

        return force_x, force_y

    def rule_alignment(self, ind, neighbors):
        adapt = ind.genome.get_val("adaptabilité")
        agilite = ind.genome.get_val("agilité")
        avg_vx = 0
        avg_vy = 0
        count = 0

        for other in neighbors:
            avg_vx += other.vx
            avg_vy += other.vy
            count += 1

        if count == 0:
            return 0, 0

        avg_vx /= count
        avg_vy /= count

        # on se rapproche doucement de la vitesse moyenne
        force_x = (avg_vx - ind.vx)
        force_y = (avg_vy - ind.vy)

        coef = (adapt / 100) * (agilite / 100) * 0.05
        force_x *= coef
        force_y *= coef

        return force_x, force_y

    def rule_cohesion(self, ind, neighbors):
        perception = ind.genome.get_val("perception")
        vitesse = ind.genome.get_val("vitesse")
        center_x = 0
        center_y = 0
        count = 0

        for other in neighbors:
            center_x += other.rect.x
            center_y += other.rect.y
            count += 1

        if count == 0:
            return 0, 0

        center_x /= count
        center_y /= count

        dx = center_x - ind.rect.x
        dy = center_y - ind.rect.y
        dist = max(1, (dx*dx + dy*dy)**0.5)

        force_x = dx / dist
        force_y = dy / dist

        coef = (perception / 100) * 0.03
        force_x *= coef
        force_y *= coef

        return force_x, force_y

    def apply_boids(self, ind, quad):
        neighbors = self.get_neighbors(ind, quad)
        if not neighbors:
            return

        sep_x, sep_y = self.rule_separation(ind, neighbors)
        ali_x, ali_y = self.rule_alignment(ind, neighbors)
        coh_x, coh_y = self.rule_cohesion(ind, neighbors)

        # combinaison des forces
        fx = sep_x + ali_x + coh_x
        fy = sep_y + ali_y + coh_y

        # mise à jour de la vitesse
        ind.vx += fx
        ind.vy += fy

        # limite de vitesse
        vitesse_max = ind.genome.get_val("vitesse")
        speed = (ind.vx*ind.vx + ind.vy*ind.vy)**0.5
        if speed > vitesse_max:
            ind.vx = ind.vx / speed * vitesse_max
            ind.vy = ind.vy / speed * vitesse_max

        # Position future anticipée
        nv_x = ind.rect.x + int(ind.vx)
        nv_y = ind.rect.y + int(ind.vy)

        # calcul du centre de l'individu 
        center_x = nv_x + ind.rect.width // 2
        center_y = nv_y + ind.rect.height // 2

        # toujours dans la fenetre pygame
        if 0 <= center_x < W and 0 <= center_y < H:
            
            # ensuite test si dans le masque ellipse
            if ALLOWED_MASK.get_at((center_x, center_y)):
                ind.rect.x = nv_x
                ind.rect.y = nv_y

            # si le boug touche le mur, on "rebondit" en inversant la vitesse
            else:
                ind.vx *= -1
                ind.vy *= -1

        else :
            #print("rebond 2")
            # sortie d'écran qui va arriver, on fait rebondir avant
            ind.vx *= -1
            ind.vy *= -1


    def handle_déplacement(self, quad, world):
        for ind in self.populations:
            self.apply_boids(ind, quad)

    # ---------- COLLISIONS / REPRO ----------

    def handle_collisions(self, quad, world):
        for ind in self.populations:
            voisins = quad.retrieve(ind.rect)

            for other in voisins:
                if other is ind:
                    continue

                if ind.collision_cooldown > 0 or other.collision_cooldown > 0: 
                    continue

                if ind.rect.colliderect(other.rect):
                    self.on_collision(ind, other, world)
                    ind.collision_cooldown = ind.collision_delay 
                    other.collision_cooldown = other.collision_delay

    def kill(self, ind):
        if ind in self.populations:
            self.populations.remove(ind)
        del ind


Population = Livings()

class Espece() :
    def __init__(self, id_espece, date_apparition):
        self.id_espece = id_espece
        self.date_apparition = date_apparition
        self.dico_evolution_alleles = {}
        self.effectif = []
        self.morte = False

        e = 0
        for l in Population.populations :
            if l.id_espece == self.id_espece :
                e += 1
        self.effectif.append(e)

        for k in dico_alleles.keys() :
            
            if dico_alleles[k][5] == "int":
                self.dico_evolution_alleles[k] = []
                t = 0
                n = 0
                for l in Population.populations :
                    if l.id_espece == self.id_espece :
                        t += l.genome.get_val(k)
                        n += 1
                
                if n != 0:
                    self.dico_evolution_alleles[k].append(t/n)

            elif dico_alleles[k][5] == "list":
                self.dico_evolution_alleles[k] = []
                t = [0,0,0]
                n = 0
                for l in Population.populations :
                    if l.id_espece == self.id_espece :
                        for i in range(3):
                            t[i] += l.genome.get_val(k)[i]
                        n += 1
                if n!=0:
                    self.dico_evolution_alleles[k].append([t[0]/n,t[1]/n,t[2]/n])
    
    def update(self):

        if not self.morte :
            e = 0
            for l in Population.populations :
                if l.id_espece == self.id_espece :
                    e += 1
            self.effectif.append(e)

            for k in dico_alleles.keys() :
                if dico_alleles[k][5] == "int":
                    t = 0
                    n = 0
                    for l in Population.populations :
                        if l.id_espece == self.id_espece :
                            t += l.genome.get_val(k)
                            n += 1
                    
                    if n!=0:
                        self.dico_evolution_alleles[k].append(t/n)

                elif dico_alleles[k][5] == "list":
                    t = [0,0,0]
                    n = 0
                    for l in Population.populations :
                        if l.id_espece == self.id_espece :
                            for i in range(3):
                                t[i] += l.genome.get_val(k)[i]
                            n += 1
                    
                    if n!=0:
                        self.dico_evolution_alleles[k].append([t[0]/n,t[1]/n,t[2]/n])