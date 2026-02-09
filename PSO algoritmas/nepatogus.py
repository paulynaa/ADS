import random
from plot_results import plot_results
import math

x_ribos = [0, 100]  
y_ribos = [0, 100]  
universitetu_sk = 3  
daleliu_sk = 500  
num_iterations = 1000  
w_inerc = 0.7 
atmintis_ind = 1.5  
globali_patirtis = 1.5 

geros_lokacijos = [
    [20,20],
    [20,80],
    [80,20],
    [80,80]
]
blogos_lokacijos = [
    [15,10],
    [30,90],
    [10,35],
    [50,40]
]

def atstumas(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def fitness_fun(*universiteto_lokacijos):
    
    universiteto_lokacijos = zip(universiteto_lokacijos[0::2], universiteto_lokacijos[1::2])
    atstumas_iki_gero = []
    atstumas_iki_blogo = []
    
    for univeras in universiteto_lokacijos:
        atstumas_iki_gero.append([atstumas(univeras, gera_l) for gera_l in geros_lokacijos])
        atstumas_iki_blogo.append([atstumas(univeras, bloga_l) for bloga_l in blogos_lokacijos])
    
    min_atstumas_iki_gero = [min(dists) for dists in zip(*atstumas_iki_gero)]
    min_atstumas_iki_blogo = [min(dists) for dists in zip(*atstumas_iki_blogo)]
    fitness = min(min_atstumas_iki_blogo) - max(min_atstumas_iki_gero)
    return fitness

class Particle:
   
    def __init__(self, bounds):
        self.pozicija = [random.uniform(bound[0], bound[1]) for bound in bounds]
        self.greitis = [random.uniform(-1, 1) for _ in bounds]
        self.best_pozicija = self.pozicija[:]
        self.best_fitness = fitness_fun(*self.pozicija)
        
    def naujas_greitis(self, global_best_pozicija, w_inerc, atmintis_ind, globali_patirtis):
        for x in range(len(self.pozicija)):
            inertia = w_inerc * self.greitis[x]
            atmintis = atmintis_ind * random.random() * (self.best_pozicija[x] - self.pozicija[x])
            globalus = globali_patirtis * random.random() * (global_best_pozicija[x] - self.pozicija[x])
            self.greitis[x] = inertia + atmintis + globalus
    
    def naujas_pozicija(self, bounds):
        for x in range(len(self.pozicija)):
            self.pozicija[x] += self.greitis[x]
            self.pozicija[x] = max(bounds[x][0], min(self.pozicija[x], bounds[x][1]))
        fitness = fitness_fun(*self.pozicija)
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_pozicija = self.pozicija[:]

class Swarm:
   
    def __init__(self, daleliu_sk, bounds, w_inerc=0.7, atmintis_ind=1.5, globali_patirtis=1.5):
        self.w_inerc = w_inerc
        self.atmintis_ind = atmintis_ind
        self.globali_patirtis = globali_patirtis
        self.bounds = bounds
        self.daleles = [Particle(self.bounds) for _ in range(daleliu_sk)]
        self.global_best_pozicija = self.daleles[0].pozicija[:]
        self.global_best_fitness = self.daleles[0].best_fitness
        
    def optimize(self, iterations):
        for _ in range(iterations):
            for dalele in self.daleles:
                dalele.naujas_greitis(self.global_best_pozicija, self.w_inerc, self.atmintis_ind, self.globali_patirtis)
                dalele.naujas_pozicija(self.bounds)
                if dalele.best_fitness > self.global_best_fitness:
                    print(f'Fit: {dalele.best_fitness}')
                    self.global_best_fitness = dalele.best_fitness
                    self.global_best_pozicija = dalele.best_pozicija[:]

bounds = [x_ribos, y_ribos] * universitetu_sk
swarm = Swarm(daleliu_sk, bounds, w_inerc, atmintis_ind, globali_patirtis)

swarm.optimize(num_iterations)
universiteto_lokacijos = [(swarm.global_best_pozicija[i], swarm.global_best_pozicija[i+1]) for i in range(0, len(swarm.global_best_pozicija), 2)]

print("\nOptimaliu universitetu koordinates:")
for idx, loc in enumerate(universiteto_lokacijos, 1):
    print(f"Universitetas {idx}: x = {loc[0]:.2f}, y = {loc[1]:.2f}")

plot_results(x_ribos, y_ribos, geros_lokacijos, blogos_lokacijos, universiteto_lokacijos)