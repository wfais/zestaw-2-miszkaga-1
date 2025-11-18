import pytest
from ZADANIE2.zadanie2 import rzymskie_na_arabskie, arabskie_na_rzymskie

def test_konwersja_minimalna_rzymska():
    assert rzymskie_na_arabskie("I") == 1

def test_konwersja_maksymalna_rzymska():
    assert rzymskie_na_arabskie("MMMCMXCIX") == 3999

def test_konwersja_minimalna_arabska():
    assert arabskie_na_rzymskie(1) == "I"

def test_konwersja_maksymalna_arabska():
    assert arabskie_na_rzymskie(3999) == "MMMCMXCIX"

def test_liczba_rzymska_z_odejmowaniem():
    assert rzymskie_na_arabskie("IV") == 4
    assert rzymskie_na_arabskie("IX") == 9
    assert rzymskie_na_arabskie("XL") == 40
    assert rzymskie_na_arabskie("XC") == 90
    assert rzymskie_na_arabskie("CD") == 400
    assert rzymskie_na_arabskie("CM") == 900

def test_liczba_rzymska_bez_odejmowania():
    assert rzymskie_na_arabskie("III") == 3
    assert rzymskie_na_arabskie("VIII") == 8
    assert rzymskie_na_arabskie("LXXX") == 80
    assert rzymskie_na_arabskie("DCCC") == 800

def test_konwersja_niemożliwa_rzymska():
    with pytest.raises(ValueError):
        rzymskie_na_arabskie("IIII")  # Powinno być IV
    with pytest.raises(ValueError):
        rzymskie_na_arabskie("VV")    # Powinno być X

def test_konwersja_nieprawidłowe_symbole():
    with pytest.raises(ValueError):
        rzymskie_na_arabskie("IC")    # Niepoprawna liczba
    with pytest.raises(ValueError):
        rzymskie_na_arabskie("ABCD")  # Niepoprawny znak

def test_arabska_poza_zakresem():
    with pytest.raises(ValueError):
        arabskie_na_rzymskie(0)       # Poza zakresem
    with pytest.raises(ValueError):
        arabskie_na_rzymskie(4000)    # Poza zakresem

def test_idempotentnosc_konwersji():
    for liczba in [1, 4, 9, 58, 1994, 3999]:
        assert rzymskie_na_arabskie(arabskie_na_rzymskie(liczba)) == liczba
