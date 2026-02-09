import numpy as np
from tabulate import tabulate

c_vector = np.array([2, -3, 0, -5, 0, 0, 0], dtype=float)

A = np.array([
    [-1,  1, -1, -1, 1, 0, 0],
    [ 2,  4,  0,  0, 0, 1, 0],
    [ 0,  0,  1,  1, 0, 0, 1]
], dtype=float)

b_salyga = np.array([8, 10, 3], dtype=float)
b_individual = np.array([9, 9, 9], dtype=float)

def simpleksas(c, A, b, baziniai):
    m, n = A.shape
    baziniai = baziniai.copy()  
    while True:
        B = A[:, baziniai]
        c_b = c[baziniai]
        B_atvirkst = np.linalg.inv(B)
        x_b = B_atvirkst @ b
        x = np.zeros(n)
        for i, idx in enumerate(baziniai):
            x[idx] = x_b[i]
        z = c_b @ B_atvirkst @ A
        reduced_costs = c - z
        if all(reduced_costs >= -1e-8):
            break
        ieinantis = np.argmin(reduced_costs)
        kryptis_d = B_atvirkst @ A[:, ieinantis]
        iseinantis = [x_b[i] / kryptis_d[i] if kryptis_d[i] > 1e-8 else np.inf for i in range(len(kryptis_d))]
        iseinancio_indeksas = np.argmin(iseinantis)
        if iseinantis[iseinancio_indeksas] == np.inf:
            break
        baziniai[iseinancio_indeksas] = ieinantis
    return x, c @ x, baziniai 

def sprendimas(A, b, c):
    pradine_baze = [4, 5, 6]  
    sol_x, z, baze = simpleksas(c, A, b, pradine_baze)
    sprend_kintam = sol_x[:4]
    si_kintam = sol_x[4:]
    return sprend_kintam, si_kintam, z, baze

sol_x, sol_s, z_sprend, baze = sprendimas(A, b_salyga, c_vector)
sol_x_indiv, sol_s_indiv, z_indiv, baze_indiv = sprendimas(A, b_individual, c_vector)

# === lentele palyg
antraste = [f"x{i+1}" for i in range(4)] + ["s1", "s2", "s3"]
sprendiniai = [
    ["Pradinis uzdavinys"] + list(np.round(sol_x, 3)) + list(np.round(sol_s, 3)) + [round(z_sprend, 3)],
    ["Individualus (9, 9, 9)"] + list(np.round(sol_x_indiv, 3)) + list(np.round(sol_s_indiv, 3)) + [round(z_indiv, 3)]
]

print("\n=== Sprendinių palyginimas ===")
print(tabulate(sprendiniai, headers=["Versija"] + antraste + ["f(X) (min)"], tablefmt="fancy_grid"))

# === baziu lentele
vardai = [f"x{i+1}" for i in range(4)] + ["s1", "s2", "s3"]
baziu_lentele = [
    ["Pradinis uzdavinys"] + [vardai[i] for i in baze],
    ["Individualus (9, 9, 9)"] + [vardai[i] for i in baze_indiv]
]
kiek_baziu = max(len(baze), len(baze_indiv))
bazes_antraste = ["Versija"] + [f"B{i+1}" for i in range(kiek_baziu)]

print("\n=== Bazės palyginimas ===")
print(tabulate(baziu_lentele, headers=bazes_antraste, tablefmt="fancy_grid"))
