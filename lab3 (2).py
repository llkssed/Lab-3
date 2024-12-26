from tkinter import *
from random import choice

# Инициализация глобальных переменных
btn = []  # Список кнопок
xBtn, yBtn = 16, 16  # Размеры игрового поля
mines = xBtn * yBtn * 10 // 64  # Количество мин
playArea = []  # Список для хранения информации о поле
nMoves = 0  # Количество ходов
mrk = 0  # Количество помеченных мин
first_move = True  # Флаг для первого хода

# Инициализация Tkinter
tk = Tk()
tk.title('Сапёр')
tk.geometry(f'{44*xBtn}x{44*yBtn+10}')

# Функция для начала игры
def play(n):
    global xBtn, yBtn, mines, nMoves, mrk, first_move
    if len(playArea) < xBtn * yBtn:  # Если поле ещё не создано
        return
    nMoves += 1
    if nMoves == 1:  # Если первый ход
        if first_move:  # Если это первый ход, ставим мины и считаем количество мин вокруг
            first_move = False
            place_mines_first_move(n)  # Функция для размещения мин, исключая первую клетку
            calculate_mines_around()

    # Обработка нажатия на кнопку
    if btn[n].cget('text') == '\u2661':  # Если клетка была помечена
        mrk -= 1
    
    btn[n].config(text=playArea[n], state=DISABLED, bg='white')  # Обновляем текст на кнопке
    if playArea[n] == 0:  # Если пустая клетка
        btn[n].config(text=' ', bg='#ccb')
        open_adjacent_cells(n)  # Открываем соседние клетки, если количество мин равно 0
    elif playArea[n] == -1:  # Если мина
        btn[n].config(text='\u2665')
        show_all_mines()  # Показываем все мины
        tk.title("Game Over")  # Выводим надпись "Game Over"
    
    # Если игрок выиграл
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:
        tk.title(f'You win!')  # Убираем таймер

# Функция для отображения всех мин после проигрыша
def show_all_mines():
    global playArea
    for i in range(len(playArea)):
        if playArea[i] == -1:  # Если это мина
            btn[i].config(text='\u2665', bg='red', state=DISABLED)

# Функция для резкого открытия соседних клеток, если вокруг 0 мин
def open_adjacent_cells(n):
    # Получаем координаты текущей клетки
    row, col = n // xBtn, n % xBtn
    # Проходим по соседям (вверх, вниз, влево, вправо, по диагоналям)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < yBtn and 0 <= c < xBtn:
                i = r * xBtn + c
                if btn[i].cget('state') != 'disabled' and playArea[i] != -1:
                    btn[i].config(text=playArea[i], state=DISABLED, bg='white')
                    if playArea[i] == 0:  # Если в соседней клетке 0 мин, открываем её соседей
                        open_adjacent_cells(i)

# Функция для победы
def winner(j):
    if j <= len(playArea):  # Если не запустили новую игру
        for i in range(j, xBtn * yBtn):
            if playArea[i] == 0:
                btn[i].config(state=NORMAL, text='☺')
                btn[i].flash()
                tk.bell()
                btn[i].config(text=' ', state=DISABLED)
                tk.after(50, winner, i + 1)
                break

# Функция для пометки клеток
def marker(n):
    global mrk, mines
    if btn[n].cget('state') != 'disabled':  # Если клетка активна
        if btn[n].cget('text') == '\u2661':  # Если уже помечена
            btn[n].config(text=' ')
            mrk -= 1
        else:
            btn[n].config(text='\u2661', fg='blue')
            mrk += 1
    
    # Если все клетки открыты и мины помечены
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:
        tk.title(f'You win!')  # Убираем таймер
        winner(0)

# Функция для старта новой игры
def new_game():
    global xBtn, yBtn, mines, nMoves, mrk, playArea, first_move
    mines = xBtn * yBtn * 10 // 64
    nMoves = 0
    mrk = 0
    first_move = True
    playArea.clear()
    # Удаляем старый фрейм, если он существует
    for widget in tk.winfo_children():
        widget.destroy()
    
    # Воссоздаём главное окно и меню
    for widget in tk.winfo_children():
        widget.destroy()
    tk.config(menu=menu_bar)
    playground()  # Создаём новое поле
    tk.title(f'Сапёр')

# Функции для изменения размера поля
def set_size(x, y):
    global xBtn, yBtn
    xBtn, yBtn = x, y
    new_game()

# Функция для создания игрового поля
def playground():
    global xBtn, yBtn
    for i in range(yBtn):
        frm = Frame(tk)
        frm.pack(expand=YES, fill=BOTH)
        for j in range(xBtn):
            button = Button(frm, text=' ', font=('mono', 16, 'bold'),
                            width=1, height=1, padx=0, pady=0)
            button.config(command=lambda n=len(btn): play(n))
            button.bind('<Button-3>', lambda event, n=len(btn): marker(n))
            button.pack(side=LEFT, expand=YES, fill=BOTH, padx=0, pady=0)
            btn.append(button)
            playArea.append(0)

# Функция для размещения мин (для первого хода)
def place_mines_first_move(first_move_index):
    global playArea
    mines_placed = 0
    while mines_placed < mines:
        j = choice(range(0, xBtn * yBtn))
        # Проверяем, что мина не будет на первой клетке
        if playArea[j] != -1 and j != first_move_index:
            playArea[j] = -1
            mines_placed += 1

# Функция для подсчёта количества мин вокруг каждой клетки
def calculate_mines_around():
    global playArea
    for i in range(xBtn * yBtn):
        if playArea[i] != -1:
            count = 0
            if i % xBtn > 0 and playArea[i - 1] == -1: count += 1
            if i % xBtn < xBtn - 1 and playArea[i + 1] == -1: count += 1
            if i >= xBtn and playArea[i - xBtn] == -1: count += 1
            if i < (xBtn * yBtn - xBtn) and playArea[i + xBtn] == -1: count += 1
            if i >= xBtn and i % xBtn > 0 and playArea[i - xBtn - 1] == -1: count += 1
            if i >= xBtn and i % xBtn < xBtn - 1 and playArea[i - xBtn + 1] == -1: count += 1
            if i < (xBtn * yBtn - xBtn) and i % xBtn > 0 and playArea[i + xBtn - 1] == -1: count += 1
            if i < (xBtn * yBtn - xBtn) and i % xBtn < xBtn - 1 and playArea[i + xBtn + 1] == -1: count += 1
            playArea[i] = count

# Меню для выбора размера поля
menu_bar = Menu(tk)
tk.config(menu=menu_bar)

game_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Новая игра", menu=game_menu)
game_menu.add_command(label="5x5", command=lambda: set_size(5, 5))
game_menu.add_command(label="8x8", command=lambda: set_size(8, 8))
game_menu.add_command(label="10x14", command=lambda: set_size(10, 14))
game_menu.add_command(label="16x16", command=lambda: set_size(16, 16))
game_menu.add_command(label="32x32", command=lambda: set_size(32, 32))

# Запуск игры
mainloop()
