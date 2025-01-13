import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

def read_mapa(filename):
    with open(filename, 'r') as file:                                       #przypisanie otwartego pliku do zmiennej file
        map_data = [list(map(int, line.strip().split())) for line in file]  #strip usuwa białe znaki i dzielimy linie na liste stringów
        return map_data


def heurestyka(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)               #nasza heuretyska

def a_gwiazdka(map_data, start, cel):
    rzedy, kol = len(map_data), len(map_data[0])
    g_score = [[float('inf')] * kol for _ in range(rzedy)]                  #na początku przypisujemy każdemu polu
    f_score = [[float('inf')] * kol for _ in range(rzedy)]                  #nieskończony koszt bo nigdzie nie dotarliśmy
    skad = [[None] * kol for _ in range(rzedy)]
    g_score[start[0]][start[1]] = 0                                         #dla pola startowego koszt zmieniami na 0
    f_score[start[0]][start[1]] = heurestyka(start, cel)
    oset = [(f_score[start[0]][start[1]], start)]                           #zestaw otwarty, krotka

    odwiedzone = []

    while oset:
        oset.sort(key=lambda x: x[0], reverse=True)                         #sortujemy po pierwszym elemencie w krotce
        obecny = oset.pop()[1]                                              #usuwamy pole z najniższym f_score i zastępujemy obecnym
        odwiedzone.append(obecny)

        if obecny == cel:
            sciezka = []                                                    #lista odtwarzająca droge od celu do startu
            while obecny:
                sciezka.append(obecny)
                obecny = skad[obecny[0]][obecny[1]]                         #skad przyszedł, współrzedne x y
            sciezka.reverse()                                               #odwracamy aby zaczynała się od startu
            return sciezka, g_score, f_score, odwiedzone

        sasiedzi = [(obecny[0] + 1, obecny[1]), (obecny[0] - 1, obecny[1]), #gora, dół
                    (obecny[0], obecny[1] + 1), (obecny[0], obecny[1] - 1)] #lewo,prawo

        for sasiad in sasiedzi:
            if 0 <= sasiad[0] < rzedy and 0 <= sasiad[1] < kol and map_data[sasiad[0]][sasiad[1]] != 5:
                                                                            #sprawdzamy czy nie jest przeszkodą
                tentative_g_score = g_score[obecny[0]][obecny[1]] + 1       #tymczasowy koszt

                if tentative_g_score < g_score[sasiad[0]][sasiad[1]]:       #jeśli jest g_score jest mniejszy
                    skad[sasiad[0]][sasiad[1]] = obecny                     #aktualizujemy skad wyszliśmy
                    g_score[sasiad[0]][sasiad[1]] = tentative_g_score
                    f_score[sasiad[0]][sasiad[1]] = tentative_g_score + heurestyka(sasiad, cel)
                                                                            #przewidywany+ heurestyka
                    oset.append((f_score[sasiad[0]][sasiad[1]], sasiad))    #dodajmy do listy

    raise Exception("Błąd 21 - Brak dostępnej ścieżki")

mapa = 'mapa.txt'
map_dane = read_mapa(mapa)
start = (0, 0)
cel = (19, 19)

start = (len(map_dane) - 1 - start[0], start[1])
cel = (len(map_dane) - 1 - cel[0], cel[1])

try:
    sciezka, g_score, f_score, odwiedzone = a_gwiazdka(map_dane, start, cel)

    if sciezka is not None:
        print("Ścieżka znaleziona")

        mapa_z_trasa = [row[:] for row in map_dane]

        for x, y in sciezka:
            mapa_z_trasa[x][y] = 2

        with open("mapa_z_trasa.txt", "w") as plik:
            for row in mapa_z_trasa:
                plik.write(" ".join(map(str, row)) + "\n")

        print("Mapa została zapisana!")

except Exception as e:
    print(e)