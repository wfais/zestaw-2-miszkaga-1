import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

# Funkcja rysująca wykres na podstawie eval()
def rysuj_wielomian(wejscie):
    # Dekompozycja danych wejściowych
    try:
        wzor_str, zakres_str = wejscie.split(',')
        x_min_str, x_max_str = zakres_str.strip().split()
        x_min = float(x_min_str)
        x_max = float(x_max_str)
    except ValueError:
        print("Błąd formatu danych. Oczekiwano: 'wzór, min max'")
        return 0, 0

    # Generowanie wartości x
    x_val = np.linspace(x_min, x_max, 200)

    # Generowanie wartości y przy użyciu eval()
    # Udostępniamy evalowi zmienną 'x' (tablicę numpy) oraz podstawowe funkcje matematyczne
    context = {
        "x": x_val,
        "sin": np.sin, "cos": np.cos, "tan": np.tan, 
        "exp": np.exp, "sqrt": np.sqrt, "log": np.log, "pi": np.pi,
        "abs": np.abs
    }
    
    try:
        y_val = eval(wzor_str, {"__builtins__": None}, context)
        
        # Jeśli wynikiem jest pojedyncza liczba (funkcja stała), zamień na tablicę
        if np.isscalar(y_val):
            y_val = np.full_like(x_val, y_val)
            
    except Exception as e:
        print(f"Błąd podczas obliczania wartości funkcji (eval): {e}")
        return 0, 0

    # Rysowanie wykresu ale bez show()
    plt.figure(figsize=(8, 6))
    plt.plot(x_val, y_val, label=f"f(x) = {wzor_str.strip()}", color='blue')
    plt.title(f"Wykres funkcji (eval): {wzor_str.strip()}")
    plt.xlabel("Oś X")
    plt.ylabel("Oś Y")
    plt.grid(True)
    plt.legend()

    # Zwracanie wartości na granicach przedziału
    return y_val[0], y_val[-1]

# Funkcja rysująca wykres na podstawie SymPy i lambdify()
def rysuj_wielomian_sympy(wejscie):
    # Dekompozycja danych wejściowych
    try:
        wzor_str, zakres_str = wejscie.split(',')
        x_min_str, x_max_str = zakres_str.strip().split()
        x_min = float(x_min_str)
        x_max = float(x_max_str)
    except ValueError:
        print("Błąd formatu danych. Oczekiwano: 'wzór, min max'")
        return 0, 0

    # Definicja symbolu i konwersja do funkcji numerycznej za pomocą SymPy
    x_sym = symbols('x')
    try:
        wyrazenie = sympify(wzor_str)
        # Konwersja na szybką funkcję NumPy
        f_numeryczna = lambdify(x_sym, wyrazenie, modules=['numpy'])
    except Exception as e:
        print(f"Błąd parsowania SymPy: {e}")
        return 0, 0

    # Generowanie wartości x
    x_val = np.linspace(x_min, x_max, 200)
    
    # Generowanie wartości y przy użyciu funkcji numerycznej
    y_val_sympy = f_numeryczna(x_val)

    # Jeśli wynikiem jest skalar (dla funkcji stałej), wypełnij tablicę
    if np.isscalar(y_val_sympy):
        y_val_sympy = np.full_like(x_val, y_val_sympy)

    # Rysowanie wykresu ale bez show()
    plt.figure(figsize=(8, 6))
    plt.plot(x_val, y_val_sympy, label=f"SymPy: {wzor_str.strip()}", color='red', linestyle='--')
    plt.title(f"Wykres funkcji (SymPy): {wzor_str.strip()}")
    plt.xlabel("Oś X")
    plt.ylabel("Oś Y")
    plt.grid(True)
    plt.legend()

    # Zwracanie wartości na granicach przedziału
    return y_val_sympy[0], y_val_sympy[-1]

if __name__ == '__main__':
    # Przykładowe wywołanie pierwszej funkcji
    wejscie1 = "x**3 + 3*x + 1, -10 10"
    
    # Pierwszy wykres z eval
    wynik_eval = rysuj_wielomian(wejscie1)
    print("Wynik (eval):", wynik_eval)
    
    # Drugie wejście dla funkcji SymPy - bardziej złożona funkcja 
    wejscie2 = "x**4 - 5*x**2 + 3*sin(x), -10 10"  
    
    # Drugi wykres z SymPy
    wynik_sympy = rysuj_wielomian_sympy(wejscie2)
    print("Wynik (SymPy):", wynik_sympy)
    
    # Wyświetlanie obu wykresów
    plt.show()