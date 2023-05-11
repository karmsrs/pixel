import tkinter as tk
from itertools import permutations
from functools import reduce
from datetime import datetime
from tkinter import messagebox


class GameData:
    class Kiwi:
        height = 15
        width = 15
        row_clues = [(1, 1),
                     (1, 1),
                     (2, 1, 1, 2),
                     (3, 3),
                     (4, 3, 1),
                     (2, 1, 4),
                     (4, 1, 2),
                     (5, 1, 1),
                     (8,),
                     (1, 6),
                     (1, 3),
                     (3, 2),
                     (2, 1),
                     (3, 1),
                     (2, 1, 1, 1)]
        col_clues = [(1,),
                     (1,),
                     (1,),
                     (1, 1),
                     (1, 3),
                     (2,),
                     (1, 4),
                     (1, 4, 1),
                     (4, 1, 1),
                     (1, 4, 1, 1),
                     (2, 2, 3, 4),
                     (5, 2, 3),
                     (3, 4, 1),
                     (1, 2, 6),
                     (1, 6, 1)]

    class Monk:
        height = 10
        width = 10
        row_clues = [(7,),
                     (3, 1, 1),
                     (2, 1, 1, 1),
                     (1, 1, 3),
                     (1, 4, 1),
                     (3, 2),
                     (3, 3),
                     (6, 1),
                     (2, 2),
                     (5, 2, 1)]
        col_clues = [(1, 2, 1),
                     (8, 1),
                     (3, 5),
                     (1, 1, 3),
                     (1, 1, 1, 1, 1),
                     (2, 2, 1),
                     (1, 1, 1, 1, 1),
                     (1, 1, 2, 2),
                     (8,),
                     (1, 1, 1)]

    class Candle:
        height = 5
        width = 5
        row_clues = [(1, 1),
                     (1, 1, 1),
                     (5,),
                     (1,),
                     (3,)]
        col_clues = [(3,),
                     (1, 1),
                     (5,),
                     (1, 1),
                     (2,)]


class Clues(tk.Frame):
    NORMAL = ('Helvetica', 12, 'bold')
    NORMAL_COLOR = 'black'
    SOLVED = ('Helvetica', 12)
    SOLVED_COLOR = 'gray70'

    STATE_COLOR_MAP = {
        NORMAL: NORMAL_COLOR,
        SOLVED: SOLVED_COLOR}

    def __init__(self, game, root, container):
        self.game = game
        self.root = root
        self.container = container
        self.state = Clues.NORMAL
        self.labels = {}
        super(Clues, self).__init__(container)

    def set_normal(self):
        self.state = Clues.NORMAL
        self.update_labels()

    def set_solved(self):
        self.state = Clues.SOLVED
        self.update_labels()

    def update_labels(self):
        if self.labels:
            for enum in self.labels.keys():
                self.labels[enum].config(font=self.state, foreground=Clues.STATE_COLOR_MAP[self.state])

    def is_solved(self):
        return self.state == Clues.SOLVED


class RowClues(Clues):
    def __init__(self, game, root, container, row, clues):
        self.row = row
        super(RowClues, self).__init__(game, root, container)
        for enum, clue in enumerate(clues):
            self.labels[enum] = tk.Label(self, text=str(clue), anchor=tk.E, font=self.state)
            if enum == 0:
                self.labels[enum].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            else:
                self.labels[enum].pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=2)


class ColClues(Clues):
    def __init__(self, game, root, container, col, clues):
        self.col = col
        super(ColClues, self).__init__(game, root, container)
        for enum, clue in enumerate(clues):
            self.labels[enum] = tk.Label(self, text=str(clue), anchor=tk.S, font=self.state)
            if enum == 0:
                self.labels[enum].pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=2)
            else:
                self.labels[enum].pack(side=tk.TOP, fill=tk.X, expand=False, pady=2)

class Mark:
    EMPTY = 'white'
    FILLED = 'black'
    POSSIBLE = 'gray70'
    BLANK = 'IndianRed1'

    SWITCH_MAP = {
        POSSIBLE: BLANK,
        BLANK: POSSIBLE}

    MARK_STATE_CHANGE_MAP = {
        FILLED: {
            EMPTY: FILLED,
            FILLED: EMPTY,
            POSSIBLE: FILLED,
            BLANK: EMPTY},
        POSSIBLE: {
            EMPTY: POSSIBLE,
            FILLED: FILLED,
            POSSIBLE: EMPTY,
            BLANK: BLANK},
        BLANK: {
            EMPTY: BLANK,
            FILLED: EMPTY,
            POSSIBLE: BLANK,
            BLANK: EMPTY}}

    MARK_TEXT_MAP = {
        FILLED: 'Mark Cell',
        POSSIBLE: 'Mark Possible',
        BLANK: 'Mark Blank'}

    STATE_VALUE_MAP = {
        EMPTY: 0,
        FILLED: 1,
        POSSIBLE: 0,
        BLANK: 0}

    STATE_SOLVED_MAP = {
        EMPTY: EMPTY,
        FILLED: FILLED,
        POSSIBLE: EMPTY,
        BLANK: EMPTY}

    def __init__(self):
        self.state = Mark.POSSIBLE

    def switch_state(self):
        self.state = Mark.SWITCH_MAP[self.state]

    def get_mark_text(self):
        return Mark.MARK_TEXT_MAP[Mark.FILLED]

    def get_state_text(self):
        return Mark.MARK_TEXT_MAP[self.state]

class Cell(tk.Frame):
    BORDER_GRAY = 'gray50'
    BORDER_BLACK = 'black'
    BORDER_BLUE = 'royal blue'
    BORDER_RED = 'coral'

    def __init__(self, game, root, container, row, col, height, width):
        self.game = game
        self.root = root
        self.container = container
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.state = Mark.EMPTY
        super(Cell, self).__init__(container)

        border_colors = {
            'nw': Cell.BORDER_GRAY,
            'n': Cell.BORDER_GRAY,
            'ne': Cell.BORDER_GRAY,
            'w': Cell.BORDER_GRAY,
            'e': Cell.BORDER_GRAY,
            'sw': Cell.BORDER_GRAY,
            's': Cell.BORDER_GRAY,
            'se': Cell.BORDER_GRAY}

        if self.row > 0 and self.row < self.height - 1:
            if self.row % 5 == 0:
                for border in ['nw', 'n', 'ne']:
                    border_colors[border] = Cell.BORDER_BLUE
            elif self.row % 5 == 4:
                for border in ['sw', 's', 'se']:
                    border_colors[border] = Cell.BORDER_BLUE
            if self.height > 10 and self.height % 10 == 0:
                if self.row % 10 == 0:
                    for border in ['nw', 'n', 'ne']:
                        border_colors[border] = Cell.BORDER_RED
                elif self.row % 10 == 9:
                    for border in ['sw', 's', 'se']:
                        border_colors[border] = Cell.BORDER_RED

        if self.col > 0 and self.col < self.width - 1:
            if self.col % 5 == 0:
                for border in ['nw', 'w', 'sw']:
                    border_colors[border] = Cell.BORDER_BLUE
            elif self.col % 5 == 4:
                for border in ['ne', 'e', 'se']:
                    border_colors[border] = Cell.BORDER_BLUE
            if self.width > 10 and self.width % 10 == 0:
                if self.col % 10 == 0:
                    for border in ['nw', 'w', 'sw']:
                        border_colors[border] = Cell.BORDER_RED
                elif self.col % 10 == 9:
                    for border in ['ne', 'e', 'se']:
                        border_colors[border] = Cell.BORDER_RED

        self.borders = {}

        top_frame = tk.Frame(self, height=1, width=32)
        self.borders['nw'] = tk.Frame(top_frame, height=1, width=1, background=border_colors['nw'])
        self.borders['nw'].pack(side=tk.LEFT)
        self.borders['n'] = tk.Frame(top_frame, height=1, width=30, background=border_colors['n'])
        self.borders['n'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.borders['ne'] = tk.Frame(top_frame, height=1, width=1, background=border_colors['ne'])
        self.borders['ne'].pack(side=tk.LEFT)
        top_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        middle_frame = tk.Frame(self, height=30, width=32)
        self.borders['w'] = tk.Frame(middle_frame, height=30, width=1, background=border_colors['w'])
        self.borders['w'].pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame = tk.Frame(middle_frame, height=30, width=30, background=self.state)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.borders['e'] = tk.Frame(middle_frame, height=30, width=1, background=border_colors['e'])
        self.borders['e'].pack(side=tk.LEFT, fill=tk.Y, expand=True)
        middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self, height=1, width=32)
        self.borders['sw'] = tk.Frame(bottom_frame, height=1, width=1, background=border_colors['sw'])
        self.borders['sw'].pack(side=tk.LEFT)
        self.borders['s'] = tk.Frame(bottom_frame, height=1, width=30, background=border_colors['s'])
        self.borders['s'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.borders['se'] = tk.Frame(bottom_frame, height=1, width=1, background=border_colors['se'])
        self.borders['se'].pack(side=tk.LEFT)
        bottom_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

    def mark_filled(self, event=None):
        self.state = Mark.MARK_STATE_CHANGE_MAP[Mark.FILLED][self.state]
        self.update()

    def mark_dynamic(self, event=None):
        self.state = Mark.MARK_STATE_CHANGE_MAP[self.game.mark.state][self.state]
        self.update()

    def update(self):
        self.frame.config(background=self.state)
        self.game.update()

    def value(self):
        return Mark.STATE_VALUE_MAP[self.state]

    def set_solved(self, event=None):
        self.state = Mark.STATE_SOLVED_MAP[self.state]
        self.frame.config(background=self.state)
        self.frame.unbind('<Button-1>')
        self.frame.unbind('<Button-3>')

    def reset(self, event=None):
        self.state = Mark.EMPTY
        self.frame.config(background=self.state)
        self.frame.unbind('<Button-1>')
        self.frame.unbind('<Button-3>')

    def start(self, event=None):
        self.frame.bind('<Button-1>', self.mark_filled)
        self.frame.bind('<Button-3>', self.mark_dynamic)


class Game:
    CELL_SIZE = 32

    def __init__(self, gamedata):
        self.height = gamedata.height
        self.width = gamedata.width
        self.row_clues = gamedata.row_clues
        self.col_clues = gamedata.col_clues
        self.mark = Mark()
        self.root = tk.Tk()
        self.root.title('Picross')
        self.root.protocol('WM_DELETE_WINDOW', self.clean_exit)
        self.root.bind('<MouseWheel>', self.switch_mark)
        self.root.iconify()

        menubar = tk.Menu(self.root)
        menubar.add_command(label='Reset', command=self.prompt_reset)
        self.root.config(menu=menubar)

        grid_height = Game.CELL_SIZE * self.height + 4
        grid_width = Game.CELL_SIZE * self.width + 4

        header_frame = tk.Frame(self.root, height=10)
        header_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        top_frame = tk.Frame(self.root, height=80)
        top_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        top_buffer = tk.Frame(self.root, height=10)
        top_buffer.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.clock_text = tk.StringVar()
        self.clock_text.set('00:00:00')

        time_label = tk.Label(top_frame, text='Time:', font=('Helvetica', 14, 'bold'))
        time_label.pack(side=tk.TOP, fill=tk.X)
        clock_label = tk.Label(top_frame, textvariable=self.clock_text, font=('Helvetica', 12, 'bold'))
        clock_label.pack(side=tk.TOP, fill=tk.X)
        
        game_frame = tk.Frame(self.root, highlightbackground='black', highlightthickness=1)
        game_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=50)
        game_frame.columnconfigure(0, weight=1)
        game_frame.rowconfigure(1, minsize=grid_height, weight=0)
        game_frame.rowconfigure(0, weight=1)
        game_frame.rowconfigure(1, minsize=grid_width, weight=0)

        bottom_buffer = tk.Frame(self.root, height=25)
        bottom_buffer.pack(side=tk.TOP, fill=tk.X, expand=True)
        bottom_frame = tk.Frame(self.root, height=100)
        bottom_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        footer_frame = tk.Frame(self.root, height=25)
        footer_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        row_clues_outer_frame = tk.Frame(game_frame)
        row_clues_outer_frame.grid(row=1, column=0, sticky=tk.NSEW)
        row_clues_container = tk.Frame(row_clues_outer_frame)
        row_clues_container.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
        for row in range(self.height):
            row_clues_container.rowconfigure(row, minsize=32, weight=0)
        self.row_clues_frames = {}
        self.row_clues_labels = {}
        for row, row_clue in enumerate(self.row_clues):
            self.row_clues_frames[row] = RowClues(self, self.root, row_clues_container, row, row_clue)
            self.row_clues_frames[row].grid(row=row, column=0, sticky=tk.NSEW)

        col_clues_outer_frame = tk.Frame(game_frame)
        col_clues_outer_frame.grid(row=0, column=1, sticky=tk.NSEW)
        col_clues_container = tk.Frame(col_clues_outer_frame)
        col_clues_container.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
        for col in range(self.width):
            col_clues_container.columnconfigure(col, minsize=32, weight=0)
        self.col_clues_frames = {}
        self.col_clues_labels = {}
        for col, col_clue in enumerate(self.col_clues):
            self.col_clues_frames[col] = ColClues(self, self.root, col_clues_container, col, col_clue)
            self.col_clues_frames[col].grid(row=0, column=col, sticky=tk.NSEW)

        grid_outer_frame = tk.Frame(game_frame, background='black')
        grid_outer_frame.grid(row=1, column=1, sticky=tk.NSEW)
        self.grid_frame = tk.Frame(grid_outer_frame)
        self.grid_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        for row in range(self.height):
            self.grid_frame.rowconfigure(row, minsize=32, weight=0)
        for col in range(self.width):
            self.grid_frame.columnconfigure(col, minsize=32, weight=0)

        self.grid = {}

        for row in range(self.height):
            self.grid[row] = {}
            for col in range(self.width):
                self.grid[row][col] = Cell(self, self.root, self.grid_frame, row, col, self.height, self.width)
                self.grid[row][col].grid(row=row, column=col, sticky=tk.NSEW)

        self.root.update()
        row_clues_container.columnconfigure(0, minsize=row_clues_container.winfo_reqwidth(), weight=0)
        col_clues_container.rowconfigure(0, minsize=col_clues_container.winfo_reqheight(), weight=0)
        bottom_frame_width = self.root.winfo_reqwidth() - 10
        split_bottom_width = bottom_frame_width // 2
        bottom_frame.columnconfigure(0, minsize=5, weight=0)
        bottom_frame.columnconfigure(1, minsize=bottom_frame_width, weight=0)
        bottom_frame.columnconfigure(2, minsize=5, weight=0)
        bottom_frame.rowconfigure(0, minsize=5, weight=0)
        bottom_frame.rowconfigure(1, minsize=45, weight=0)
        bottom_frame.rowconfigure(2, minsize=45, weight=0)
        bottom_frame.rowconfigure(3, minsize=5, weight=0)

        left_click_frame = tk.Frame(bottom_frame)
        left_click_frame.grid(row=1, column=1, sticky=tk.NSEW)
        left_click_frame.rowconfigure(0, minsize=45, weight=0)
        left_click_frame.columnconfigure(0, minsize=split_bottom_width, weight=0)
        left_click_frame.columnconfigure(1, minsize=split_bottom_width, weight=0)

        left_click_label = tk.Label(left_click_frame, text='Left Click:', font=('Helvetica', 10, 'bold'), anchor=tk.E)
        left_click_label.grid(row=0, column=0, sticky=tk.NSEW)
        left_click_frame_right = tk.Frame(left_click_frame)
        left_click_frame_right.grid(row=0, column=1, sticky=tk.NSEW)
        left_click_mark_frame = tk.Frame(left_click_frame_right, height=30, width=30, background=Mark.FILLED)
        left_click_mark_frame.pack(side=tk.TOP)
        left_click_mark_label = tk.Label(left_click_frame_right, text=self.mark.get_mark_text(), font=('Helvetica', 8))
        left_click_mark_label.pack(side=tk.TOP)

        self.right_click_mark = tk.StringVar()
        self.right_click_mark.set(self.mark.get_state_text())

        right_click_frame = tk.Frame(bottom_frame)
        right_click_frame.grid(row=2, column=1, sticky=tk.NSEW)
        right_click_frame.rowconfigure(0, minsize=45, weight=0)
        right_click_frame.columnconfigure(0, minsize=split_bottom_width, weight=0)
        right_click_frame.columnconfigure(1, minsize=split_bottom_width, weight=0)

        right_click_frame_left = tk.Frame(right_click_frame)
        right_click_frame_left.grid(row=0, column=0, sticky=tk.NSEW)
        right_click_label_top = tk.Label(right_click_frame_left, text='Right Click:', font=('Helvetica', 10, 'bold'), anchor=tk.E)
        right_click_label_top.pack(side=tk.TOP, fill=tk.X)
        right_click_label_bottom = tk.Label(right_click_frame_left, text='(scroll changes)', font=('Helvetica', 8, 'bold'), anchor=tk.E)
        right_click_label_bottom.pack(side=tk.TOP, fill=tk.X)
        right_click_frame_right = tk.Frame(right_click_frame)
        right_click_frame_right.grid(row=0, column=1, sticky=tk.NSEW)
        self.right_click_mark_frame = tk.Frame(right_click_frame_right, height=30, width=30, background=self.mark.state)
        self.right_click_mark_frame.pack(side=tk.TOP)
        right_click_mark_label = tk.Label(right_click_frame_right, textvariable=self.right_click_mark, font=('Helvetica', 8))
        right_click_mark_label.pack(side=tk.TOP)

        self.prompt_start()
        self.root.mainloop()

    def update(self):
        for row in range(self.height):
            cells = [(self.grid[row][col].value(), self.width - (col + 1)) for col in range(self.width)]
            not_empty = reduce(lambda a, b: (a[0] + b[0], 0), cells)[0]
            value = reduce(lambda a, b: ((a[0] << a[1]) + (b[0] << b[1]), 0), cells)[0]
            clue = self.row_clues[row]
            if not_empty == sum(clue) and value in self.possibles(clue, self.width):
                self.set_solved(row=row)
            else:
                self.set_normal(row=row)

        for col in range(self.width):
            cells = [(self.grid[row][col].value(), self.height - (row + 1)) for row in range(self.height)]
            not_empty = reduce(lambda a, b: (a[0] + b[0], 0), cells)[0]
            value = reduce(lambda a, b: ((a[0] << a[1]) + (b[0] << b[1]), 0), cells)[0]
            clue = self.col_clues[col]
            if not_empty == sum(clue) and value in self.possibles(clue, self.height):
                self.set_solved(col=col)
            else:
                self.set_normal(col=col)

        self.check_solved()

    def possibles(self, clues, length):
        def blank_distributions(blanks, range_start=1):
            yield (blanks,)
            for i in range(range_start, blanks // 2 + 1):
                for p in blank_distributions(blanks - i, i):
                    yield (i,) + p

        def floating_distributions(floating_blanks, possible_blank_locations):
            distributions = [distribution + (0,) * (possible_blank_locations - len(distribution))
                             for distribution
                             in blank_distributions(floating_blanks)
                             if len(distribution) <= possible_blank_locations]
            return reduce(lambda a, b: a + b, map(lambda d: list(set(permutations(d))), distributions))

        total_blanks = length - sum(clues)
        possible_blank_locations = len(clues) + 1
        mandatory_blank_locations = len(clues) - 1
        floating_blanks = total_blanks - mandatory_blank_locations
        mandatory_blanks = (0,) + (1,) * mandatory_blank_locations + (0,)

        _clues = clues[::-1]
        possibles = []
        for possible_floating_blanks in floating_distributions(floating_blanks, possible_blank_locations):
            blanks = list(map(lambda x, y: x + y, mandatory_blanks, possible_floating_blanks))[-1:0:-1]
            offset = 0
            possible = 0
            for enum, blank in enumerate(blanks):
                offset += blank
                possible += int('1' * _clues[enum], 2) << offset
                offset += _clues[enum]
            possibles.append(possible)
        return possibles

    def set_normal(self, row=None, col=None):
        if row is not None:
            self.row_clues_frames[row].set_normal()
        elif col is not None:
            self.col_clues_frames[col].set_normal()

    def set_solved(self, row=None, col=None):
        if row is not None:
            self.row_clues_frames[row].set_solved()
        elif col is not None:
            self.col_clues_frames[col].set_solved()

    def check_solved(self):
        if all(self.row_clues_frames[row].is_solved() for row in range(self.height)) and all(self.col_clues_frames[col].is_solved() for col in range(self.width)):
            self.complete()

    def complete(self):
        self.root.after_cancel(self.timer)
        elapsed = datetime.utcfromtimestamp((datetime.now() - self.start_time).total_seconds())
        self.clock_text.set(elapsed.strftime('%H:%M:%S.%f'))
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].set_solved()
        if messagebox.showinfo('Complete!', f'Congratulations!\n\nTime taken: {elapsed.strftime("%H:%M:%S.%f")}'):
            pass
        self.clean_exit()


    def switch_mark(self, event=None):
        self.mark.switch_state()
        self.right_click_mark_frame.config(background=self.mark.state)
        self.right_click_mark.set(self.mark.get_state_text())

    def tick(self, event=None):
        elapsed = datetime.utcfromtimestamp((datetime.now() - self.start_time).total_seconds())
        self.clock_text.set(elapsed.strftime('%H:%M:%S'))
        self.timer = self.root.after(1000, self.tick)

    def prompt_start(self, event=None):
        self.root.deiconify()
        if messagebox.askyesno('Ready to Start?', 'Are you ready to begin?'):
            self.start()
        else:
            self.clean_exit()

    def start(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].start()
        self.update()
        self.start_time = datetime.now()
        self.timer = self.root.after(1000, self.tick)

    def prompt_reset(self, event=None):
        if messagebox.askyesno('Restart?', 'Do you wish to restart?'):
            self.reset()

    def reset(self):
        self.root.after_cancel(self.timer)
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].reset()
        self.clock_text.set('00:00:00')
        self.start()

    def clean_exit(self, event=None):
        self.root.destroy()


if __name__ == '__main__':
    Game(GameData.Kiwi)
    # Game(GameData.Monk)
    # Game(GameData.Candle)
