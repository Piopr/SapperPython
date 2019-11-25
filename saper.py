import random, os

def get_number_of_mines(field_size):
    """Funkcja pobiera od użytkownika i zwraca liczbę min.
        Sprawdza, czy została podana liczba całkowita.
        Funkcja pobiera rozmiar pola."""
    while (True):
        try:
            mines = int(input("Podaj liczbę min na planszy: "))
        except ValueError:
            print("Nie wprowadzono liczby calkowitej")
        else:
            if mines >= field_size and mines < 1:
                print("BLAD! Wpisz poprawna liczbe min: ")
            else:
                return mines

def deploy_mines(mines, width, height):
    """Funkcja tworzy tablicę dwuwymiarową i uzupełnia ją minami w losowych miejscach.
        Pobiera jako argumenty ilosc min, szerokosc i wysokość pola.
        Zwraca tablicę z minami."""
    #tymczasowa tablica, która będzie zwracana. wartość 9 = mina w tym polu.
    tmparr=[[0 for x in range(width)] for y in range(height)]
    tmpMines=mines#do kontroli, czy obsadzono wszystkie miny
    while(True):
        if tmpMines==0:
            return tmparr
        # zmienne do losowania pozycji min
        tmpx = random.randint(0, height - 1)
        tmpy = random.randint(0, width - 1)
        #print("Wkladam do x: ", tmpx, " y:", tmpy)
        if 0 == tmparr[tmpx][tmpy]:
            tmparr[tmpx][tmpy]=9
            tmpMines-=1

def number_of_neighboring_mines(zMinami, x, y):
    """
    Funkcja zwraca ilość min na sąsiednich polach.
    Jako parametry przyjmuje kolejno:
    tablica z minami
    współrzędne aktualnie sprawdzanej komórki (x,y)
    """
    nom=0### number of mines
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i==0 and j==0) or x+i<0 or y+j<0:
                pass
            else:
                try:
                    zMinami[x+i][y+j]==9
                except IndexError:
                    pass
                else:
                    if int(zMinami[x+i][y+j])==9:
                        nom+=1
    return nom

def create_board(zMinami):
    """
    Funkcja uzupełnia tablicę z minami ustawiając pozostałe pola ilością min w polach dookoła.
    Przyjmuje tablicę z minami.
    Zwraca uzupełnioną tablicę.
    """
    height= len(zMinami)
    width= len(zMinami[0])
    for i in range(height):
        for j in range(width):
            if zMinami[i][j]==0:
                zMinami[i][j]=number_of_neighboring_mines(zMinami, i, j)
    return zMinami


def reveal_squears(tabGlowna, tabCzyOdkryte, x, y):
    """
    Funkcja do odkrywania pól.
    Jako argumenty przyjmuje:
    :param tabGlowna: tablica z minami oraz ilością min na sąsiednich polach
    :param tabCzyOdkryte: tablica monitorująca już odkryte pola. Potrzebna do wyświetlania.
    :param x: współrzędna odkrywanego pola
    :param y: współrzędna odkrywanego pola
    :return: nic
    """
    if tabGlowna[x][y]!=0:
            tabCzyOdkryte[x][y]=1
    else:
        #tabCzyOdkryte[x][y] = 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or x + i < 0 or y + j < 0 or x+i>len(tabGlowna)-1 or y+j>len(tabGlowna[0])-1:
                    tabCzyOdkryte[x][y] = 1
                else:
                    if tabCzyOdkryte[x+i][y+j]==0:
                        tabCzyOdkryte[x + i][y + j] = 1
                        reveal_squears(tabGlowna, tabCzyOdkryte, x+i, y+j)
        #reveal_squears(tabGlowna, tabCzyOdkryte, i, j)

def print_board(tabGlowna, tabCzyOdkryte):
    kolumny=" "
    for z in range(len(tabGlowna)):
        kolumny+=str(z)
        kolumny+=" "
    print(kolumny)
    print((" " + chr(9473)) * len(tabGlowna))
    rzad=" "
    for i in range(len(tabGlowna[0])):
        rzad = chr(9475)
        for j in range(len(tabGlowna)):
            if tabCzyOdkryte[i][j]==0:
                rzad += " " #gdy nieodkryte
                rzad += chr(9475)
            else:
                if tabGlowna[i][j]==9:
                    rzad += "*"
                    rzad += chr(9475)
                elif tabGlowna[i][j]==0:
                    rzad += "0" #gdy odkryte
                    rzad += chr(9475)
                else:
                    rzad += str(tabGlowna[i][j])
                    rzad += chr(9475)
        print(rzad+str(i))
        print((" " + chr(9473)) * len(tabGlowna))

def is_over(tabCzyOdkryte):
    """
    sprawdza, czy koniec gry (czy odkryto wszystkie wolne pola)
    :return: liczba już odkrytych pól
    """
    tmp_control=0
    for i in range(len(tabCzyOdkryte)):
        for j in range(len(tabCzyOdkryte[0])):
            if tabCzyOdkryte[i][j]==1:
                tmp_control+=1
    return tmp_control

def sapper():
    while(True):
        try:
            width = int(input("Podaj szerokość: "))
        except ValueError:
            print("Nie wprowadzono liczby calkowitej")
        else:
            break
    while(True):
        try:
            height = int(input("Podaj wysokosc: "))
        except ValueError:
            print("Nie wprowadzono liczby calkowitej")
        else:
            break
    mines = get_number_of_mines(width*height)
    tab_with_mines = deploy_mines(mines, width, height)
    tab_final = create_board(tab_with_mines)
    ### Tworzenie tablicy, ktora zawiera informacje, czy pola powinny byc wyswietlane
    tabCzyOdkryte = [[0 for x in range(width)] for y in range(height)]
    #os.system('cls')
    #os.system('clear')
    kontrola_konca_gry = height*width-mines #liczba pol, na ktorych nie ma min. Jesli tyle pol odkrytych, to wygrana
    print_board(tab_final, tabCzyOdkryte)
    while(True):        
        while (True):
            try:
                x = int(input("Podaj wspolrzedna y do odkrycia: "))
            except ValueError:
                print("Nie wprowadzono liczby calkowitej")
            else:
                break
        while (True):
            try:
                y = int(input("Podaj wspolrzedna x do odkrycia: "))
            except ValueError:
                print("Nie wprowadzono liczby calkowitej")
            else:
                break
        if tab_final[x][y]==9:
            reveal_squears(tab_final, tabCzyOdkryte, x, y)
            print_board(tab_final, tabCzyOdkryte)
            print("Przegrales!")
            break
        else:
            reveal_squears(tab_final, tabCzyOdkryte, x, y)
            print_board(tab_final,  tabCzyOdkryte)
            if kontrola_konca_gry == is_over(tabCzyOdkryte):
                print("Gratulacje! Wygrales!")
                break

if __name__ == '__main__':
    sapper()

