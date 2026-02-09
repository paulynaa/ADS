import numpy as np
import matplotlib.pyplot as plt
from sympy import *

def tikslofunkcija(x, a=9, b=9):
    return ((x**2 - a)**2) / b - 1

def intervalo_dal_pusiau(f, l, r, tiksl=1e-4):
    iter = 0
    fun_ivertinimu = 0

    xm = (l + r) / 2
    L = r - l
    f_xm = f(xm)
    fun_ivertinimu += 1
    while L > tiksl:
        x1 = l + L / 4
        x2 = r - L / 4
        f_x1, f_x2 = f(x1), f(x2)
        fun_ivertinimu += 2

        if f_x1 < f_xm:
            r = xm
            xm = x1
            f_xm = f_x1
        elif f_x2 < f_xm:
            l = xm
            xm = x2
            f_xm = f_x2
        else:
            l = x1
            r = x2
        
        L = r - l
        iter += 1

    x_min = xm
    f_min = f_xm

    return x_min, f_min, iter, fun_ivertinimu


# intervalas [0,10]
int_apatinis, int_virsutinis = 0, 10

# x_min, f_min, iter, fun_ivertinimu = intervalo_dal_pusiau(tikslofunkcija, int_apatinis, int_virsutinis)
# dalijimo pusiau  grafikas
x_reiks = np.linspace(int_apatinis, int_virsutinis, 1000)
y_reiks = tikslofunkcija(x_reiks)

x_test_pusiau = []
x_min, f_min, iter, fun_ivertinimu = intervalo_dal_pusiau(
    lambda x: x_test_pusiau.append(x) or tikslofunkcija(x), int_apatinis, int_virsutinis
)

plt.figure(figsize=(10, 6))
plt.plot(x_reiks, y_reiks, label='f(x)', color='blue', linewidth=2)
plt.scatter(x_test_pusiau, [tikslofunkcija(x) for x in x_test_pusiau], color='orange', label='Bandymo taškai')
plt.scatter([x_min], [f_min], color='red', label=f'Rasto minimumo taško x={x_min:.4f}', s=100)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Intervalo dalijimo pusiau grafikas')
plt.legend()
plt.grid()
plt.show()

print("Intervalo dalijimo pusiau metodas:")
print(f"Rasto minimumo tasko x = {x_min:.4f}")
print(f"Rasko minimumo tasko f(x) = {f_min:.4f}")
print(f"Iteraciju skaicius: {iter}")
print(f"Funkciju ivertinimu skaicius: {fun_ivertinimu}")



# niutono metodas

def niutono_met(f, x0, tiks=1e-4, max_iter=1000):
    x = symbols('x')
    f_sym = f(x)
    f_isvestine = Derivative(f_sym, x).doit()
    f_antra_isv = Derivative(f_isvestine, x).doit()

    f_func = lambdify(x, f_sym, 'numpy')
    f_isvestine_func = lambdify(x, f_isvestine, 'numpy')
    f_antra_isv_func = lambdify(x, f_antra_isv, 'numpy')

    itera = 0
    funkc_iv = 0
    x_dabar = x0
    bandymo_taskai = [x_dabar] 

    while itera < max_iter:
        f_isvest_reiksme = f_isvestine_func(x_dabar)
        f_antra_isv_reiks = f_antra_isv_func(x_dabar)
        itera += 1
        funkc_iv += 2
        if abs(f_isvest_reiksme) < tiks:
            break

        if f_antra_isv_reiks == 0:
            print("Klaida")
            break

        x_naujas = x_dabar - f_isvest_reiksme / f_antra_isv_reiks
        bandymo_taskai.append(x_naujas) 

        if abs(x_naujas - x_dabar) < tiks:
            break
        
        x_dabar = x_naujas

    return x_dabar, f_func(x_dabar), itera, funkc_iv, bandymo_taskai


# niutono grafikas
x_test_niuton = []
f_num = lambda x: x_test_niuton.append(x) or tikslofunkcija(x)

# m
x0=5
x_min_n, f_min_n, iter_n, iv_n, x_test_niuton = niutono_met(tikslofunkcija, x0)

plt.figure(figsize=(10, 6))
plt.plot(x_reiks, y_reiks, label='f(x)', color='blue', linewidth=2)
plt.scatter(x_test_niuton, [tikslofunkcija(x) for x in x_test_niuton], color='orange', label='Bandymo taškai')
plt.scatter([x_min_n], [f_min_n], color='red', label=f'Rasto minimumo taško x={x_min_n:.4f}', s=100)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Niutono metodo eiga')
plt.legend()
plt.grid()
plt.show()

print("Niutono Metodas:")
print(f"Rasto minimumo tasko x = {x_min_n:.4f}")
print(f"Rasto minimumo tasko f(x) = {f_min_n:.4f}")
print(f"Iteraciju skaicius: {iter_n}")
print(f"Funkciju ivertinimu skaicius: {iv_n}")


# auksinio pjuvio met
def auksinis_pjuvis(f, l, r, tiksl=1e-4):
    tau = (np.sqrt(5) - 1) / 2
    iter = 0
    fun_ivertinimu = 0

    x1 = r - tau * (r - l)
    x2 = l + tau * (r - l)
    f_x1, f_x2 = f(x1), f(x2)
    fun_ivertinimu += 2

    x_test_auksinis = [x1, x2]

    while (r - l) > tiksl:
        if f_x1 < f_x2:
            r = x2
            x2 = x1
            f_x2 = f_x1
            x1 = r - tau * (r - l)
            f_x1 = f(x1)
        else:
            l = x1
            x1 = x2
            f_x1 = f_x2
            x2 = l + tau * (r - l)
            f_x2 = f(x2)

        fun_ivertinimu += 1
        iter += 1
        x_test_auksinis.append(x1 if f_x1 < f_x2 else x2)

    x_min = (l + r) / 2
    f_min = f(x_min)

    return x_min, f_min, iter, fun_ivertinimu, x_test_auksinis

x_test_auksinis = []
x_min_a, f_min_a, iter_a, fun_ivertinimu_a, x_test_auksinis = auksinis_pjuvis(
    lambda x: tikslofunkcija(x), int_apatinis, int_virsutinis
)

# auksinio pjuvio grafikas
plt.figure(figsize=(10, 6))
plt.plot(x_reiks, y_reiks, label='f(x)', color='blue', linewidth=2)
plt.scatter(x_test_auksinis, [tikslofunkcija(x) for x in x_test_auksinis], color='purple', label='Bandymo taškai')
plt.scatter([x_min_a], [f_min_a], color='red', label=f'Rasto minimum taško x={x_min_a:.4f}', s=100)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Auksinio pjūvio metodo grafikas')
plt.legend()
plt.grid()
plt.show()

print("Auksinio pjuvio metodas:")
print(f"Rasto minimumo tasko x = {x_min_a:.4f}")
print(f"Rasto minimumo tasko f(x) = {f_min_a:.4f}")
print(f"Iteraciju skaicius: {iter_a}")
print(f"Funkciju ivertinimu skaicius: {fun_ivertinimu_a}")
