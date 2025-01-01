import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

def read_mapa(filename):
    with open(filename, 'r') as file:
        map_data = [list(map(int, line.strip().split())) for line in file]
    return map_data

def heurestyka(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def a_gwiazdka(map_data, start, cel):
    rzedy, kol = len(map_data), len(map_data[0])
    g_score = [[float('inf')] * kol for _ in range(rzedy)]
    f_score = [[float('inf')] * kol for _ in range(rzedy)]
    skad = [[None] * kol for _ in range(rzedy)]
    g_score[start[0]][start[1]] = 0
    f_score[start[0]][start[1]] = heurestyka(start, cel)
    oset = [(f_score[start[0]][start[1]], start)]

    odwiedzone = []

    while oset:
        oset.sort(key=lambda x: x[0], reverse=True)
        obecny = oset.pop()[1]
        odwiedzone.append(obecny)

        if obecny == cel:
            sciezka = []
            while obecny:
                sciezka.append(obecny)
                obecny = skad[obecny[0]][obecny[1]]
            sciezka.reverse()
            return sciezka, g_score, f_score, odwiedzone

        sasiedzi = [(obecny[0] + 1, obecny[1]), (obecny[0] - 1, obecny[1]),
                    (obecny[0], obecny[1] + 1), (obecny[0], obecny[1] - 1)]

        for sasiad in sasiedzi:
            if 0 <= sasiad[0] < rzedy and 0 <= sasiad[1] < kol and map_data[sasiad[0]][sasiad[1]] != 5:
                tentative_g_score = g_score[obecny[0]][obecny[1]] + 1

                if tentative_g_score < g_score[sasiad[0]][sasiad[1]]:
                    skad[sasiad[0]][sasiad[1]] = obecny
                    g_score[sasiad[0]][sasiad[1]] = tentative_g_score
                    f_score[sasiad[0]][sasiad[1]] = tentative_g_score + heurestyka(sasiad, cel)
                    oset.append((f_score[sasiad[0]][sasiad[1]], sasiad))

    raise Exception("Błąd 21 - Brak dostępnej ścieżki")

def wizualizuj_animacje(map_dane, odwiedzone, sciezka, g_score, f_score):
    grid = np.array(map_dane)

    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = plt.cm.colors.ListedColormap(['white', 'blue', 'red', 'green', 'gray'])
    przedzialy = [0, 1, 2, 3, 4, 6]
    norm = plt.cm.colors.BoundaryNorm(przedzialy, cmap.N)

    im = ax.imshow(grid, cmap=cmap, norm=norm, extent=[-0.5, grid.shape[1] - 0.5, -0.5, grid.shape[0] - 0.5])

    plt.xticks(np.arange(grid.shape[1]) - 0.5, labels=np.arange(grid.shape[1]))
    plt.yticks(np.arange(grid.shape[0]) - 0.5, labels=np.arange(grid.shape[0]))
    plt.grid(True, color='black', linewidth=0.5)
    plt.title("Obliczanie f_score dla każdego pola")

    all_texts = {}
    current_step = [0]

    def update(frame):
        if current_step[0] < len(odwiedzone):
            x, y = odwiedzone[current_step[0]]

            grid[x][y] = 3  # Oznacza odwiedzone pole na mapie
            im.set_data(grid)

            sasiedzi = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for sasiad in sasiedzi:
                if (0 <= sasiad[0] < grid.shape[0] and 0 <= sasiad[1] < grid.shape[1]
                        and map_dane[sasiad[0]][sasiad[1]] != 5):
                    f_value = f_score[sasiad[0]][sasiad[1]]
                    if f_value != float('inf') and (sasiad[0], sasiad[1]) not in all_texts:
                        text = ax.text(sasiad[1], grid.shape[0] - 1 - sasiad[0], f"{f_value:.2f}",
                                       ha='center', va='center', color='black', fontsize=6)
                        all_texts[(sasiad[0], sasiad[1])] = text

            current_step[0] += 1
        elif current_step[0] == len(odwiedzone):
            for x, y in sciezka:
                grid[x][y] = 2  # Oznacza ścieżkę na mapie
            im.set_data(grid)
            current_step[0] += 1

        return [im] + list(all_texts.values())

    ani = animation.FuncAnimation(fig, update, frames=len(odwiedzone) + 1, interval=20, repeat=False) #przy dużej mapie
    plt.show()                                                                                        #lepiej dać > 50

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
        wizualizuj_animacje(map_dane, odwiedzone, sciezka, g_score, f_score)

except Exception as e:
    print(e)
