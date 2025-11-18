import os
import time
import threading
import sys

LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    suma_czesciowa = 0.0
    
    for i in range(pocz, kon):
        x = (i + 0.5) * krok
        suma_czesciowa += 4.0 / (1.0 + x * x)
        
    wyniki[indeks] = suma_czesciowa


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW:,}\n")

    krok = 1.0 / LICZBA_KROKOW
    wyniki = [0.0]
    w = threading.Thread(target=policz_fragment_pi, args=(0, LICZBA_KROKOW, krok, wyniki, 0))
    w.start()
    w.join()

    czas_referencyjny = 0.0

    print(f"{'Wątki':<10} {'Przybliżenie Pi':<20} {'Czas [s]':<15} {'Przyspieszenie':<15}")
    print("-" * 65)

    for liczba_watkow in LICZBA_WATKOW:
        wyniki = [0.0] * liczba_watkow
        watki = []
        
        czesc = LICZBA_KROKOW // liczba_watkow
        
        start_czas = time.perf_counter()

        for i in range(liczba_watkow):
            poczatek = i * czesc
            koniec = (i + 1) * czesc if i != liczba_watkow - 1 else LICZBA_KROKOW
            
            w = threading.Thread(
                target=policz_fragment_pi,
                args=(poczatek, koniec, krok, wyniki, i)
            )
            watki.append(w)
            w.start()

        for w in watki:
            w.join()

        stop_czas = time.perf_counter()
        
        pi_total = sum(wyniki) * krok
        czas_trwania = stop_czas - start_czas

        if liczba_watkow == 1:
            czas_referencyjny = czas_trwania
            przyspieszenie = 1.00
        else:
            przyspieszenie = czas_referencyjny / czas_trwania

        print(f"{liczba_watkow:<10} {pi_total:<20.10f} {czas_trwania:<15.4f} {przyspieszenie:<15.2f}x")

if __name__ == "__main__":
    main()