def rzymskie_na_arabskie(rzymskie):
    """
    Konwertuje liczbę rzymską (str) na arabską (int).
    Weryfikuje poprawność znaków oraz składni rzymskiej.
    """
    # Sprawdzenie typu
    if not isinstance(rzymskie, str):
        raise ValueError("Wejście musi być łańcuchem znaków.")
    
    # Mapa wartości
    mapa = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    
    # Sprawdzenie czy zawiera tylko poprawne znaki
    for znak in rzymskie:
        if znak not in mapa:
            raise ValueError(f"Niepoprawny znak w liczbie rzymskiej: {znak}")
            
    # Algorytm konwersji
    suma = 0
    prev_value = 0
    
    # Iterujemy od końca, co upraszcza logikę odejmowania (IV: 1 < 5 -> odejmij)
    for znak in reversed(rzymskie):
        curr_value = mapa[znak]
        if curr_value < prev_value:
            suma -= curr_value
        else:
            suma += curr_value
        prev_value = curr_value
        
    # WALIDACJA POPRAWNOŚCI FORMATU (Round-trip check)
    # Algorytm powyżej policzy 'IIII' jako 4, ale to nie jest poprawny rzymski zapis.
    # Sprawdzamy to, konwertując wynik z powrotem na rzymski.
    # Jeśli wynik się różni od wejścia (np. IV != IIII), zgłaszamy błąd.
    try:
        poprawny_rzymski = arabskie_na_rzymskie(suma)
        if poprawny_rzymski != rzymskie:
            raise ValueError(f"Niepoprawny format liczby rzymskiej: {rzymskie} (powinno być {poprawny_rzymski})")
    except ValueError:
        # Przechwytuje błędy z arabskie_na_rzymskie (np. wynik poza zakresem)
        raise ValueError(f"Wartość liczby rzymskiej {rzymskie} wykracza poza zakres obsługi.")

    return suma

def arabskie_na_rzymskie(arabskie):
    """
    Konwertuje liczbę arabską (int) na rzymską (str).
    Obsługuje zakres 1-3999.
    """
    # Sprawdzenie typu
    if not isinstance(arabskie, int):
        raise ValueError("Wejście musi być liczbą całkowitą.")
        
    # Sprawdzenie zakresu
    if not (1 <= arabskie <= 3999):
        raise ValueError(f"Liczba {arabskie} spoza zakresu 1-3999.")
    
    # Tabela konwersji (od największych do najmniejszych)
    # Uwzględniamy przypadki odejmowania (CM, CD, XC itp.) dla zwięzłości kodu
    wartosci = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    wynik = []
    
    for wartosc, symbol in wartosci:
        # Dopóki liczba jest większa lub równa wartości symbolu, dodajemy symbol
        while arabskie >= wartosc:
            wynik.append(symbol)
            arabskie -= wartosc
            
    return "".join(wynik)

if __name__ == '__main__':
    try:
        # Przykłady konwersji rzymskiej na arabską
        rzymska = "MCMXCIV"
        print(f"Liczba rzymska {rzymska} to {rzymskie_na_arabskie(rzymska)} w arabskich.")
        
        # Test błędnego formatu (odkomentuj aby sprawdzić)
        # print(rzymskie_na_arabskie("IIII")) 
        
        # Przykłady konwersji arabskiej na rzymską
        arabska = 1994
        print(f"Liczba arabska {arabska} to {arabskie_na_rzymskie(arabska)} w rzymskich.")
        
        # Test błędnego zakresu (odkomentuj aby sprawdzić)
        # print(arabskie_na_rzymskie(4000))

    except ValueError as e:
        print(f"Błąd: {e}")