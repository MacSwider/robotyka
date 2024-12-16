import matplotlib.pyplot as plt  # Biblioteka do tworzenia wykresów
import numpy as np  # Biblioteka do obliczeń numerycznych
import math  # Biblioteka matematyczna

def read_mapa(filename):  # Wczytuje plik tekstowy od końca do początku
    with open(filename, 'r') as file:
        map_data = [list(map(int, line.strip().split())) for line in file.readlines()[::-1]]
    return map_data

def heurestyka(x, y):  # Heurystyka oparta na metryce euklidesowej
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def a_gwiazdka(map_data, start, cel):
    rzedy, kol = len(map_data), len(map_data[0])  # Wymiary mapy
    oset = [(0, start)]  # Lista zawierająca węzły do odwiedzenia
    skad = {}  # Słownik śledzi skąd przyszedł algorytm do danego węzła
    g_score = {start: 0}  # Koszt dotarcia do każdego węzła od start
    f_score = {start: heurestyka(start, cel)}  # Przewidywany całkowity koszt

    while oset:
        # Znajdź węzeł z najmniejszą wartością f w liście otwartej
        obecny = min(oset, key=lambda x: x[0])[1]
        oset = [item for item in oset if item[1] != obecny]

        if obecny == cel:
            sciezka = []
            while obecny in skad:
                sciezka.append(obecny)
                obecny = skad[obecny]
            sciezka.append(start)
            sciezka.reverse()
            return sciezka

        # Kolejność obczajania sąsiadów: góra, dół, lewo, prawo
        sasiedzi = [(obecny[0] + 1, obecny[1]), (obecny[0] - 1, obecny[1]),
                    (obecny[0], obecny[1] + 1), (obecny[0], obecny[1] - 1)]

        for sasiad in sasiedzi:
            if 0 <= sasiad[0] < rzedy and 0 <= sasiad[1] < kol and map_data[sasiad[0]][sasiad[1]] != 5:
                tentative_g_score = g_score[obecny] + 1  # Potencjalny koszt dojścia

                if sasiad not in g_score or tentative_g_score < g_score[sasiad]:
                    skad[sasiad] = obecny
                    g_score[sasiad] = tentative_g_score
                    f_score[sasiad] = tentative_g_score + heurestyka(sasiad, cel)
                    oset.append((f_score[sasiad], sasiad))

    raise Exception("Błąd 21 - Brak dostępnej scieżki")  # Podnoszenie wyjątku w przypadku braku ścieżki

def sciezka_zapis(map_dane, sciezka, plik):  # Zaznacza ścieżkę na mapie i zapisuje do pliku
    for x, y in sciezka:
        map_dane[x][y] = 3

    # Zaznacz start i cel na mapie
    start, cel = sciezka[0], sciezka[-1]
    map_dane[start[0]][start[1]] = 1    # Zaznaczamy obydwa punkty na czerwono
    map_dane[cel[0]][cel[1]] = 1        # Patrz 75 linijka
    #odwrocona_mapa = map_dane[::-1]
    with open(plik, 'w') as file:
        for line in map_dane:
            file.write(' '.join(map(str, line)) + '\n')

def wizualizuj(plik):  # POTEŻNA FUNKCJA DO WRZUCENIA NA WYKRES

    with open(plik, 'r') as f:  # Wczytanie dane z pliku
        dane = f.readlines()

    grid = [list(map(int, line.strip().split())) for line in dane]  # Przekształcenie dane na listę liczb

    grid = np.array(grid)  # Konwersja gridu na tablice

    plt.figure(figsize=(7, 7))  # Tworzenie wykresu 7x7

    # Definicja kolorów
    # 0 - biały (dostępne miejsca),
    # 1 - czerwony (początek),
    # 3 - zielony (ścieżka),
    # 5 - szary (przeszkody)
    cmap = plt.cm.colors.ListedColormap(['white', 'red', 'green', 'gray']) #tworzenie kolormapy
    przedzialy = [0, 1, 3, 4, 6]  # Przedziały dla wartości
    norm = plt.cm.colors.BoundaryNorm(przedzialy, cmap.N)

    # Rysowanie siatki z przesunięciem o 0,5 jednostki w obu osiach
    plt.imshow(grid, cmap=cmap, norm=norm, extent=[-0.5, grid.shape[1] - 0.5, -0.5, grid.shape[0] - 0.5])

    # Ustawienia osi wykresu
    # tick (zaznaczenia na osiach) to małe znaczniki na skali osi, które pomagają w odczytywaniu wartości na wykresie
    plt.xticks(np.arange(grid.shape[1]) - 0.5, labels=np.arange(grid.shape[1]))       #przesunięcie siatki o 0.5 w lewo
    plt.yticks(np.arange(grid.shape[0]) + 0.5, labels=np.arange(grid.shape[0])[::-1]) #przesunięcie o 0.5 w dól [::-1]odwraca oś
    plt.gca().invert_yaxis()
    plt.grid(True, color='black', linewidth=0.5)
    plt.title("Gotowa trasa z punktu startowego do celu")
    plt.show()

mapa = 'mapa.txt'  # Wczytujemy mapę

map_dane = read_mapa(mapa)
start = (0, 0)  # Współrzędne wpisujemy (Y, X) nie (X, Y)
cel = (19, 19)

try:
    sciezka = a_gwiazdka(map_dane, start, cel)

    if sciezka is not None:
        mapa_ze_sciezka = 'map_ze_sciezka.txt'
        sciezka_zapis(map_dane, sciezka, mapa_ze_sciezka)
        print("Ścieżka znaleziona i zapisana w", mapa_ze_sciezka)
        wizualizuj(mapa_ze_sciezka)

except Exception as e:
    print(e)

