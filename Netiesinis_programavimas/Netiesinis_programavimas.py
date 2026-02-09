import numpy as np
from tabulate import tabulate # type: ignore


X0 = np.array([0.0, 0.0, 0.0])
X1 = np.array([1.0, 1.0, 1.0])
Xm = np.array([9 / 10, 9 / 10, 9 / 10])

def f(X):
    x, y, z = X
    return -x * y * z 

def g(X):
    x, y, z = X
    return 2 * (x * y + y * z + x * z) - 1  

def h(X):
    x, y, z = X
    return [-x, -y, -z]  

def B(X, r):
    bauda_kv = g(X)**2 + sum(max(0, hi)**2 for hi in h(X))
    return f(X) + (1.0 / max(r, 1e-4)) * bauda_kv  

def grad_B(X, r, h_step=1e-5):
    grad = np.zeros(3)
    fx = B(X, r)
    for i in range(3):
        X_step = X.copy()
        X_step[i] += h_step
        grad[i] = (B(X_step, r) - fx) / h_step
    return grad

def gradient_nusileidimas(f, grad_f, X0, zings=0.01, epsilon=1e-6, max_iter=15000):
    X = np.array(X0, dtype=float) + 1e-4
    kelias = [X.copy()]
    i = 1
    kvietimai = 0
    while i < max_iter:
        grad = grad_f(X)
        kvietimai += 1
        grad_norm = np.linalg.norm(grad)
        if grad_norm <= epsilon:
            break
        grad = grad / grad_norm 

        alpha = zings
        while f(X - alpha * grad) > f(X) - 1e-4 * alpha * grad_norm**2 and alpha > 1e-8:
            alpha *= 0.7

        X = X - alpha * grad
        X = np.clip(X, 1e-6, 1e+2)
        kelias.append(X.copy())
        i += 1
    return X, f(X), i, kvietimai, np.array(kelias)

def funkciju_reiks():
    print(" Pradiniai taskai ir funkciju reiksmes ")
    duom = []
    for name, X in zip(["X0", "X1", "Xm"], [X0, X1, Xm]):
        gx = g(X)
        hx = h(X)
        duom.append([
            name,
            *[round(x, 4) for x in X],
            round(f(X), 3),
            round(gx, 3),
            "[" + ", ".join(f"{hi:.1f}" for hi in hx) + "]"
        ])
    antrast = ["Taškas", "x", "y", "z", "f(X)", "g(X)", "h(X)"]
    print(tabulate(duom, headers=antrast, tablefmt="fancy_grid"))

def sprendiniai(X_start):
    r_visi = [10.0, 1.0, 0.5, 0.1, 0.01, 0.001]
    rez = []
    X_dabartinis = np.array(X_start)
    for r in r_visi:
        grad_f_r = lambda X: grad_B(X, r)
        f_r = lambda X: B(X, r)
        X_opt, f_val, iters, kv, _ = gradient_nusileidimas(f_r, grad_f_r, X_dabartinis, zings = 0.001 if r > 0.01 else 0.01)
        X_dabartinis = X_opt
        rez.append([
            f"{r:.1e}",
            *[round(xi, 4) for xi in X_opt],
            round(f(X_opt), 4),
            round(g(X_opt),4),
            iters,
            kv
        ])
    return rez

def visi_sprend():
    pradiniai_task = {"X0": X0, "X1": X1, "Xm": Xm}
    for label, X in pradiniai_task.items():
        print(f"\n--- Lentele su pradiniu tasku {label} ---")
        lentel = sprendiniai(X)
        antrast = ["r", "x", "y", "z", "f(X)", "g(X)", "Iteracijos", "Skaičiavimai"]
        print(tabulate(lentel, headers=antrast, tablefmt="fancy_grid"))

if __name__ == "__main__":
    funkciju_reiks()
    visi_sprend()
