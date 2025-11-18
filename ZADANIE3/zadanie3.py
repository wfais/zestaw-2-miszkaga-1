import requests, re, time, sys
from collections import Counter

URL = "https://pl.wikipedia.org/api/rest_v1/page/random/summary"
N = 100  # liczba losowań
HEADERS = {
    "User-Agent": "wp-edu-wiki-stats/0.1 (kontakt: twoj-email@domena)",
    "Accept": "application/json",
}

# przygotowanie wyrażenia regularnego wyłapującego słowa (litery)
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def selekcja(text: str):
    """
    Zwraca listę słów wydobytych z 'text', spełniających warunki:
     - słowa zapisane małymi literami
     - długość każdego słowa > 3 znaki
    """
    if not text:
        return []
        
    # Znajdź wszystkie dopasowania (same litery), zamień na małe i filtruj długość
    znalezione = WORD_RE.findall(text)
    return [slowo.lower() for slowo in znalezione if len(slowo) > 3]


def ramka(text: str, width: int = 80) -> str:
    """
    Zwraca napis w ramce o stałej szerokości.
    """
    # Obliczamy dostępną szerokość na tekst (bez nawiasów [])
    inner_width = width - 2
    
    # Jeśli tekst jest za długi, przycinamy go i dodajemy wielokropek
    if len(text) > inner_width:
        # Przycinamy tak, aby zmieścił się wielokropek (width - 2 - 1 = width - 3)
        text = text[:inner_width - 1] + "…"
    
    # Centrujemy tekst w dostępnej przestrzeni
    centered_text = text.center(inner_width)
    
    return f"[{centered_text}]"


def main():
    cnt = Counter()
    licznik_slow = 0
    pobrane = 0

    # linia statusu (początkowa)
    print(ramka("Start"), end="", flush=True)

    while pobrane < N:
        try:
            response = requests.get(URL, headers=HEADERS, timeout=10)
            response.raise_for_status() # Sprawdza czy status HTTP jest 200 OK
            data = response.json()
        except Exception:
            # timeout / brak JSON / błąd sieci → spróbuj ponownie
            time.sleep(0.1)
            continue

        # 1. Pobierz tytuł
        title = data.get("title") or ""
        
        # 2. Wydrukuj ramkę z tytułem (z \r na początku, aby nadpisywać linię)
        line = "\r" + ramka(title, 80)
        print(line, end="", flush=True)

        # 3. Pobierz treść i przetwórz
        extract = data.get("extract") or ""
        lista_slow = selekcja(extract)
        
        # 4. Aktualizuj liczniki
        cnt.update(lista_slow)
        licznik_slow += len(lista_slow)
        pobrane += 1
        
        # Opcjonalna krótka przerwa dla płynności wyświetlania
        # time.sleep(0.05)

    # Nowa linia po zakończeniu pętli (żeby nie pisać w linii z ramką)
    print() 
    print(f"Pobrano: {pobrane}")
    print(f"#Słowa:  {licznik_slow}")
    print(f"Unikalne:  {len(cnt)}\n")

    print("Najczęstsze 15 słów:")
    # Wypisanie 15 najczęstszych słów
    # most_common zwraca listę krotek np. [('słowo', 10), ('inne', 8)]
    for slowo, ilosc in cnt.most_common(15):
        print(f"{slowo}: {ilosc}")

if __name__ == "__main__":
    main()