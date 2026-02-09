import numpy as np
import matplotlib.pyplot as plt
from sympy import *

def tikslo_funkcija(X):
    x1, x2 = X
    return - x1 * x2 * (1 - x1 - x2)/8

def gradientas(X):
    x1, x2 = X
    df_dx1 = - 1/8 *(x2 - x2**2 - 2 * x1 * x2)
    df_dx2 = - 1/8*( x1 - x1**2 - 2 * x1 * x2)
    return np.array([df_dx1, df_dx2])


def gradient_nusileidimas(f, grad_f, X0, zings=3.0, epsilon=1e-6, max_iter=1000):
    X = np.array(X0, dtype=float)
    kelias = [X.copy()]
    i = 0
    kvietimai = 0  
    
    while i < max_iter:
        grad = grad_f(X)  
        kvietimai += 1  
        if np.linalg.norm(grad) <= epsilon:
            break
        X -= zings * grad
        kelias.append(X.copy())
        i += 1
    
    return X, f(X), i, kvietimai, np.array(kelias)  


X0 = np.array([0.0, 0.0])
X1 = np.array([1.0, 1.0])
Xm = np.array([0.9, 0.9])

# Gradientinio nusileidimo rezultatai
results_gd = {}
for X_init in [X0, X1, Xm]:
    X_min, f_min, zin, fk, kelias = gradient_nusileidimas(tikslo_funkcija, gradientas, X_init)
    results_gd[tuple(X_init)] = (X_min, f_min, zin, fk, kelias)

print("Gradientinis nusileidimas--------------------------------")
for X_init, (X_sol, f_val, iterations, kvietimai, _) in results_gd.items():
    X_init_fmt = tuple(round(float(coord), 4) for coord in X_init)
    X_sol_fmt = tuple(round(float(coord), 4) for coord in X_sol)
    print(f"Pradinis taskas: {X_init_fmt}")
    print(f"f(x) = {round(f_val,4)}")
    print(f"Rastas minimumo taskas: {X_sol_fmt}")
    print(f"Iteraciju skaicius: {iterations}")
    print(f"Funkcijos kvietimu skaicius: {kvietimai}\n")

def niutono_met(f, x0, tiks=1e-4, max_iter=100):
    x = symbols('x')
    f_sym = f(x)
    f_prim = Derivative(f_sym, x).doit()
    f_antra = Derivative(f_prim, x).doit()

    f_func = lambdify(x, f_sym, 'numpy')
    f_prim_func = lambdify(x, f_prim, 'numpy')
    f_antra_func = lambdify(x, f_antra, 'numpy')

    x_dabar = x0

    for _ in range(max_iter):
        p = f_prim_func(x_dabar)
        pp = f_antra_func(x_dabar)

        if abs(p) < tiks or pp == 0 or pp < 0:
            break

        x_naujas = x_dabar - p / pp

        if abs(x_naujas - x_dabar) < tiks:
            break

        x_dabar = x_naujas

    return max(x_dabar, 1e-6)  

def greiciausias_nusileidimas(X0, gradientas, tikslo_funkcija, max_iter=200, tol=1e-5):
    X = np.array(X0, dtype=float)
    kelias = [X.copy()]
    i = 0
    kvietimai = 0
    paskutine_reiksme = tikslo_funkcija(X)

    while i < max_iter:
        grad = gradientas(X)
        kvietimai += 1
        norm_grad = np.linalg.norm(grad)
        if norm_grad < tol:
            break

        def phi(opt_zings):
            return tikslo_funkcija(X - opt_zings * grad)

        opt_zings = niutono_met(phi, 1.0)

        X -= opt_zings * grad
        dabartine_reiksme = tikslo_funkcija(X)
        kelias.append(X.copy())

        if abs(paskutine_reiksme - dabartine_reiksme) < 1e-7:
            break

        paskutine_reiksme = dabartine_reiksme
        i += 1

    return X, paskutine_reiksme, i, kvietimai, kelias


results_gn = {}
for X_init in [X0, X1, Xm]:
    X_min, f_min, zin, fk, kelias = greiciausias_nusileidimas(X_init, gradientas, tikslo_funkcija)
    results_gn[tuple(X_init)] = (X_min, f_min, zin, fk, kelias)

print("Greiciausias nusileidimas--------------------------------")
for X_init, (X_sol, f_val, iterations, kvietimai, _) in results_gn.items():
    X_init_fmt = tuple(round(float(coord), 4) for coord in X_init)
    X_sol_fmt = tuple(round(float(coord), 4) for coord in X_sol)
    print(f"Pradinis taskas: {X_init_fmt}")
    print(f"f(x) = {round(f_val,4)}")
    print(f"Rastas minimumo taskas: {X_sol_fmt}")
    print(f"Iteraciju skaicius: {iterations}")
    print(f"Funkcijos kvietimu skaicius: {kvietimai}\n")
    

def deformuojamo_simplekso(X0, max_iter=1000, tol=1e-6):
    alpha, gamma, rho, sigma = 1.0, 3.0, 0.5, 0.5
    n = len(X0)
    laikina_virsune1 = (np.sqrt(n+1) + n-1)/(n*np.sqrt(2)) * 0.1
    laikina_virsune2 = (np.sqrt(n+1) - 1)/(n*np.sqrt(2)) * 0.1
    
    simpleksas = np.array([
        X0,
        [X0[0] + laikina_virsune1, X0[1] + laikina_virsune2],
        [X0[0] + laikina_virsune2, X0[1] + laikina_virsune1]
    ])
    kelias = [X0.copy()]
    kvietimai = 0
    for _ in range(max_iter):
        reiksmes = np.array([tikslo_funkcija(p) for p in simpleksas])
        indeksai = np.argsort(reiksmes)
        simpleksas = simpleksas[indeksai] 
        centroidas = np.mean(simpleksas[:-1], axis=0)
        atspindys = centroidas + alpha * (centroidas - simpleksas[-1])
        kvietimai += 1
        if tikslo_funkcija(atspindys) < reiksmes[indeksai[0]]:
            ispletimas = centroidas + gamma * (atspindys - centroidas)
            kvietimai += 1
            simpleksas[-1] = ispletimas if tikslo_funkcija(ispletimas) < tikslo_funkcija(atspindys) else atspindys
        else:
            if tikslo_funkcija(atspindys) < reiksmes[indeksai[1]]:
                simpleksas[-1] = atspindys
            else:
                suspaudimas = centroidas + rho * (simpleksas[-1] - centroidas)
                kvietimai += 1
                simpleksas[-1] = suspaudimas if tikslo_funkcija(suspaudimas) < reiksmes[indeksai[-1]] else simpleksas[0] + sigma * (simpleksas - simpleksas[0])
        
        kelias.append(simpleksas[0].copy())

        kelias.append(simpleksas[-1].copy())
        kelias.append(simpleksas[1].copy())
        if np.max(np.linalg.norm(simpleksas - centroidas, axis=1)) < tol:
            break
    
    return simpleksas[0], tikslo_funkcija(simpleksas[0]), len(kelias), np.array(kelias), kvietimai



    # Deformuoto simplekso metodo rezultatai
results_ds = {}
for X_init in [X0, X1, Xm]:
    X_min, f_min, zin, kelias, kvietimai = deformuojamo_simplekso(X_init)
    results_ds[tuple(X_init)] = (X_min, f_min, zin, kelias, kvietimai)

print("Deformuotas Simpleksas-----------------------------------")
for X_init, (X_sol, f_val, iterations, _, kvietimai) in results_ds.items():
    X_init_fmt = tuple(round(float(coord), 4) for coord in X_init)
    X_sol_fmt = tuple(round(float(coord), 4) for coord in X_sol)
    print(f"Pradinis taskas: {X_init_fmt}")
    print(f"f(x) = {round(f_val,4)}")
    print(f"Rastas minimumo taskas: {X_sol_fmt}")
    print(f"Iteraciju skaicius: {iterations}")
    print(f"Funkcijos kvietimu skaicius: {kvietimai}\n")

def plot_optimization(paths, method_name):
    x = np.linspace(-0.1, 1.1, 100)
    y = np.linspace(-0.1, 1.1, 100)
    X, Y = np.meshgrid(x, y)
    Z = tikslo_funkcija([X, Y])
    
    plt.figure(figsize=(8, 6))
    plt.contour(X, Y, Z, levels=20, cmap='viridis', linewidths=0.5)
    plt.colorbar(label='f(x)')
    
    markers = ['o', 's', '^']
    colors = ['r', 'b', 'g']
    
    for i, (start_point, path) in enumerate(paths.items()):
        path = np.array(path)
        start_point_fmt = tuple(round(float(coord), 4) for coord in start_point)
        plt.plot(path[:, 0], path[:, 1], linestyle='-', marker=markers[i], color=colors[i], label=f'Pradžia: {start_point_fmt}')
        plt.scatter(path[-1, 0], path[-1, 1], color='purple', marker='x', s=100, label='Rastas minimumo taskas' if i == 0 else "")
    
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title(f'{method_name} optimizacijos trajektorija')
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

# Gradientinio nusileidimo trajektorijos
keliai_gd = {tuple(X_init): kelias for X_init, (_, _, _, _, kelias) in results_gd.items()}
plot_optimization(keliai_gd, 'Gradientinis nusileidimas')

# Greičiausio nusileidimo trajektorijos
keliai_gn = {tuple(X_init): kelias for X_init, (_, _, _, _, kelias) in results_gn.items()}
plot_optimization(keliai_gn, 'Greičiausias nusileidimas')

# Deformuoto Simplekso trajektorijos
keliai_ds = {tuple(X_init): kelias for X_init, (_, _, _, kelias, _) in results_ds.items()}
plot_optimization(keliai_ds, 'Deformuotas Simpleksas')