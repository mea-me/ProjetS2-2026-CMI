import pygame
from .genome import Genome
from random import choice, randint
from .allele import Allele
from .individu import Individu
from .optimisation import QuadTree
from .environnement import WorldMap


class Livings:
    def __init__(self):
        self.populations = []

    def add_individu(self,individu):
        self.populations.append(individu)
    
    def reproduction(self, individu1, individu2,world):
        new_genome = Genome()

        for allele1, allele2 in zip(individu1.genome.alleles, individu2.genome.alleles):
            
            if allele1.type in ('str', 'list'):
                parent_allele = choice([allele1, allele2]) # choisir l'allèle du parent 1 ou 2

                if isinstance(parent_allele.valeur, list): 
                    valeur = parent_allele.valeur.copy() 
                else: 
                    valeur = parent_allele.valeur

                new_allele = Allele(parent_allele.nom,
                                    parent_allele.al_type, 
                                    parent_allele.req, 
                                    valeur, 
                                    parent_allele.mutation_rate, 
                                    parent_allele.mutation_step,
                                    parent_allele.type)
                
            if allele1.type == 'int':
                gosse_value = (allele1.valeur + allele2.valeur)//2
                parent_allele = choice([allele1, allele2]) # choisir l'allèle du parent 1 ou 2

                new_allele = Allele(parent_allele.nom, 
                                    parent_allele.al_type, 
                                    parent_allele.req, 
                                    gosse_value, 
                                    parent_allele.mutation_rate, 
                                    parent_allele.mutation_step,
                                    parent_allele.type)
                
                
            new_genome.add_allele(new_allele)

        # Position du bébé entre les parents ça marche pas trop
        x = (individu1.rect.x + individu2.rect.x) // 2
        y = (individu1.rect.y + individu2.rect.y) // 2

        #new_genome.muter() # Fait muter le génome
        bébé = Individu(x, y) # Création du nouvel individu
        bébé.give_genome(new_genome.clone())
        bébé.genome.muter()
        self.populations.append(bébé) # Ajout à la population
        #test d'environement
        bébé.give_rect(bébé.genome.get_val("taille"))
        temp = bébé.genome.get_val("température")
        hum = bébé.genome.get_val("humidité")
        env = world.get_infos_at(bébé.x,bébé.y)
        if abs(env[1]-temp) >= 5:
            if randint(0,100)<5:
                self.kill(bébé)
        elif abs(env[1]-temp) >= 10:
            if randint(0,100)<20:
                self.kill(bébé)
        

    def on_collision(self, ind1, ind2, world):
        env1 = world.get_infos_at(ind1.x,ind1.y)
        env2 = world.get_infos_at(ind2.x,ind2.y)
        temp1 = ind1.genome.get_val("température")
        temp2 = ind2.genome.get_val("température")
        hum1 = ind1.genome.get_val("humidité")
        hum2 = ind2.genome.get_val("humidité")
        if ind1.age >= 3 and ind2.age >=3 and ind1.age <= 8 and ind2.age <= 8:
            if abs(env1[1]-temp1) < 5 and abs(env2[1]-temp2) < 5:
                self.reproduction(ind1,ind2,world)
            elif abs(env1[1]-temp1) < 10 and abs(env2[1]-temp2) < 10:
                if randint(0,100)<75:
                    self.reproduction(ind1,ind2,world)
            elif abs(env1[1]-temp1) < 15 and abs(env2[1]-temp2) < 20:
                if randint(0,100)<20:
                    self.reproduction(ind1,ind2,world)
        # reproduction, combat, échange génétique, etc.

    def update(self, screen_width, screen_height, world):
        # Mettre à jour les cooldowns 
        for ind in self.populations: 
            if ind.collision_cooldown > 0: 
                ind.collision_cooldown -= 1/60

        # Créer le QuadTree
        quad = QuadTree(0, pygame.Rect(0, 0, screen_width, screen_height))
        quad.clear()

        #Insérer tous les individus
        for ind in self.populations:
            quad.insert(ind)
            ind.update()
            if not(ind.is_alive()):
                self.kill(ind) 

        #  Gérer les interactions
        self.handle_collisions(quad, world)

    def handle_collisions(self, quad, world):
        for ind in self.populations:
            #récupére uniquement les individus proches
            voisins = quad.retrieve(ind.rect)

            for other in voisins:
                if other is ind:
                    continue

                #Ignore si cooldon actif 
                if ind.collision_cooldown > 0 or other.collision_cooldown > 0: 
                    continue

                #Collision
                if ind.rect.colliderect(other.rect):
                    self.on_collision(ind, other, world)

                    # Activer cooldown pour les deux
                    ind.collision_cooldown = ind.collision_delay 
                    other.collision_cooldown = other.collision_delay

    def kill(self,ind):
        self.populations.pop(self.populations.index(ind))
        del ind
