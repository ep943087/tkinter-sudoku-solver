from tkinter import *
from tkinter import messagebox

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.geometry("450x450")
        self.resizable(False,False)
        self.button_color = "blue"
        self.solved_color = "#00cc00"
        self.default_color = "black"

        self.init_solve_button()
        self.init_board()
        self.init_buttons()

        self.sudoku_board = []
    def copy_board(self):
        self.sudoku_board.clear()
        self.sudoku_board = []
        for i in range(9):
            tmp = []
            for j in range(9):
                value = self.sudoku[i][j].get()
                if(len(value)>0):
                    value = int(value)
                else:
                    value = 0
                tmp.append(value)
            self.sudoku_board.append(tmp)
        self.make_board_black()
    def print_board(self):
        for row in self.sudoku_board:
            print(row)
    def make_board_black(self):
        for i in range(9):
            for j in range(9):
                self.sudoku[i][j]["fg"] = self.default_color
    def solve(self):
        """
            backtracking algorithm is used to solve
        """
        self.copy_board()      
        past = []
        goback = False
        i = 0
        while(i<9):
            j = 0
            while(j<9):
                if(self.sudoku_board[i][j]!=0 and not goback):
                    j+=1
                else:
                    goback = False
                    self.sudoku_board[i][j] +=1 
                    while(self.sudoku_board[i][j]<=9 and not self.check(i,j)):
                        self.sudoku_board[i][j]+=1
                    if(self.sudoku_board[i][j]>9):
                        if(len(past)==0):
                            messagebox.showinfo(title="Error",message="Could not solve sudoku puzzle")
                            return
                        self.sudoku_board[i][j] = 0
                        i,j = past[-1][0],past[-1][1]
                        past.pop()
                        goback = True
                    else:
                        past.append((i,j))
            i+=1
        self.copy(self.sudoku_board)
        self.focus()
        for i,j in past:
            self.sudoku[i][j]["fg"] = self.solved_color
    def check(self,i,j):
        if(self.sudoku_board[i][j]==0):
            return True
        return (self.check_row(i,j) and 
                self.check_column(i,j) and
                self.check_section(i,j))


    def check_section(self,i,j):
        x = i//3*3
        y = j//3*3
        m,n = x,y
        value = self.sudoku_board[i][j]
        for m in range(x,x+3):
            for n in range(y,y+3):
                if(m==i and n==j):
                    continue
                if(self.sudoku_board[m][n]==value):
                    return False
        return True
    def check_row(self,i,j):
        value = self.sudoku_board[i][j]
        for k in range(9):
            if(k==j):
                continue
            if(self.sudoku_board[i][k]==value):
                return False
        return True
    def check_column(self,i, j):
        value = self.sudoku_board[i][j]
        for k in range(9):
            if(k==i):
                continue
            if(self.sudoku_board[k][j]==value):
                return False
        return True        
    def init_solve_button(self):
        btn = Button(self,text="Solve",command=self.solve,fg=self.solved_color)
        btn.pack()
    def init_board(self):
        si = 0
        sj = 0

        self.sections_frame = Frame(self)
        self.sections_frame.pack()
        self.sections = []
        for i in range(3):
            tmp = []
            for j in range(3):
                sec = Frame(self.sections_frame,borderwidth=2,relief="groove")
                sec.config(bg=self.default_color)
                sec.grid(row=i,column=j)
                tmp.append(sec)
            self.sections.append(tmp)               
        self.sudokuFrame = Frame(self)
        self.sudokuFrame.pack()

        self.sudoku = []
        for i in range(9):
            tmp = []
            for j in range(9):
                ent = Entry(self.sections[i//3][j//3],width=2,justify="center")
                ent.bind("<Key>",lambda e,i=i,j=j: self.check_input(i,j,e)) 
                ent.grid(row=si+i,column=sj+j)
                tmp.append(ent)
            self.sudoku.append(tmp)

        self.sudoku[0][0].focus()
    def reset(self):
        for i in range(9):
            for j in range(9):
                self.sudoku[i][j].delete(0,END)
        self.make_board_black()
        self.focus()
    def copy(self,board):
        for i in range(9):
            for j in range(9):
                self.sudoku[i][j].delete(0,END)
                if board[i][j]!=0:
                    self.sudoku[i][j].insert(0,str(board[i][j]))
        self.make_board_black()
        self.focus()
    def easy(self):
        easy = [
            [0,7,0,0,0,0,0,0,9],
            [5,1,0,4,2,0,6,0,0],
            [0,8,0,3,0,0,7,0,0],
            [0,0,8,0,0,1,3,7,0],
            [0,2,3,0,8,0,0,4,0],
            [4,0,0,9,0,0,1,0,0],
            [9,6,2,8,0,0,0,3,0],
            [0,0,0,0,1,0,4,0,0],
            [7,0,0,2,0,3,0,9,6]
        ]
        self.copy(easy)
    def medium(self):
        med = [
            [0,0,0,8,3,2,0,9,0],
            [0,0,0,0,0,5,7,0,6],
            [1,0,0,6,0,0,0,0,0],
            [3,0,0,0,0,0,0,0,0],
            [6,7,4,0,0,0,8,5,1],
            [0,0,0,0,0,0,0,0,7],
            [0,0,0,0,0,1,0,0,5],
            [9,0,2,5,0,0,0,0,0],
            [0,3,0,2,7,6,0,0,0]
        ]
        self.copy(med)
    def hard(self):
        hard = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]   
        ]
        self.copy(hard)
    def impossible(self):
        imp = [
            [8,0,0,0,0,0,0,0,0],
            [0,0,3,6,0,0,0,0,0],
            [0,7,0,0,9,0,2,0,0],
            [0,5,0,0,0,7,0,0,0],
            [0,0,0,0,4,5,7,0,0],
            [0,0,0,1,0,0,0,3,0],
            [0,0,1,0,0,0,0,6,8],
            [0,0,8,5,0,0,0,1,0],
            [0,9,0,0,0,0,4,0,0]
        ]
        self.copy(imp)

    def init_buttons(self):
        self.buttons = Frame(self)
        self.buttons.pack()
        easy = Button(self.buttons,text="Easy",command=self.easy,fg=self.button_color)
        easy.grid(row=0,column=1)
        med = Button(self.buttons,text="Medium",command=self.medium,fg=self.button_color)
        med.grid(row=0,column=2)        
        hard = Button(self.buttons,text="Hard",command=self.hard,fg=self.button_color)
        hard.grid(row=0,column=3)
        imp = Button(self.buttons,text="Impossible",command=self.impossible,fg=self.button_color)
        imp.grid(row=0,column=4)
        reset = Button(self,text="Reset",command=self.reset,fg="red")
        reset.pack()
    def check_input_after(self,i,j,e):
        self.make_board_black()
        if(e.char=='\t'):
            return
        value = self.sudoku[i][j].get()
        length = len(value)
        if(length>1):
            self.sudoku[i][j].delete(0,END)
            self.sudoku[i][j].insert(0,value[0:1])
        elif(e.char<"1" or e.char>"9"):
            self.sudoku[i][j].delete(0,END)
        elif(not self.check_board(i,j)):
            self.sudoku[i][j].delete(0,END)

    def check_board(self,i,j):
        self.copy_board()
        for m in range(9):
            for n in range(9):
                if(not self.check(m,n)):
                    return False
        return True
    def check_input(self,i,j,e):
        self.after(5, lambda e=e,i=i,j=j:self.check_input_after(i,j,e))

    def run(self):
        self.mainloop()