import threading
from tkinter import *
import time


class GUI:
    def __init__(self, my_color, FEN):
        self.FEN = FEN
        self.my_color = my_color
        self.square_size = 70
        self.frame_width = 250
        self.label_width = 25
        self.window_width = self.square_size * 8 + self.frame_width + 2 * self.label_width
        self.window_height = self.square_size * 8 + 2 * self.label_width
        self.cells_canvases = []
        self.cells_pieces = [[{"type":"", "ImgObj":None} for j in range(8)] for i in range(8)]
        self.Image_files = {}
        self.even_color = "#d78500"
        self.odd_color = "#ffde81"
        self.label_frame_color = "#8e4200"
        self.side_frame_color = "#55FF00"
        self.window = Tk()
        self.window.title("Chess Game")
        self.window.minsize(width=self.window_width, height=self.window_height)
        self.window.maxsize(width=self.window_width, height=self.window_height)
        self.window.resizable(width=FALSE, height=FALSE)
        self.construct_layout()

    def construct_layout(self):
        # creating label frame1
        self.label_frame1 = Frame(self.window, width=self.label_width, height=self.window_height,
                                  bg=self.label_frame_color)
        self.label_frame1.place(anchor=NW, x=0, y=0)

        # creating label frame2
        self.label_frame2 = Frame(self.window, width=self.square_size * 8, height=self.label_width,
                                  bg=self.label_frame_color)
        self.label_frame2.place(anchor=NW, x=self.label_width, y=0)

        # creating label frame3
        self.label_frame3 = Frame(self.window, width=self.label_width, height=self.window_height,
                                  bg=self.label_frame_color)
        self.label_frame3.place(anchor=NW, x=self.label_width + 8 * self.square_size, y=0)

        # creating label frame4
        self.label_frame4 = Frame(self.window, width=self.square_size * 8, height=self.label_width,
                                  bg=self.label_frame_color)
        self.label_frame4.place(anchor=NW, x=self.label_width, y=self.label_width + 8 * self.square_size)

        # creating board frame
        self.board_frame = Frame(self.window, width=8 * self.square_size, bg="orange", height=8 * self.square_size)
        self.board_frame.place(anchor=NW, x=self.label_width, y=self.label_width)

        # creating calculations frame
        self.Frame1 = Frame(self.window, width=self.frame_width, bg=self.side_frame_color, height=self.window_height)
        self.Frame1.place(anchor=NE, x=self.window_width, y=0)

        # Adding counters
        self.Fmove_count = 0
        self.Fmove_title = Label(self.Frame1, text="Full-Move counter:", font=("Helvetica", 15), bg="red")
        self.Fmove_title.place(anchor=NW, x=14, y=10)
        self.Fmove_value_label = Label(self.Frame1, text="0", font=("Helvetica", 15), bg="red")
        self.Fmove_value_label.place(anchor=NW, x=190, y=10)

        self.Hmove_count = 0
        self.Hmove_title = Label(self.Frame1, text="Half-Move counter:", font=("Helvetica", 15), bg="red")
        self.Hmove_title.place(anchor=NW, x=10, y=40)
        self.Hmove_value_label = Label(self.Frame1, text="0", font=("Helvetica", 15), bg="red")
        self.Hmove_value_label.place(anchor=NW, x=190, y=40)

        # win/lose/Draw msgs
        self.msg = Label(self.window, text="Draw", pady=30, padx=20, font=("Helvetica", 70, "bold"), bg="red")

        #adding the numbering frame around board
        self.Add_labels()

        #create board structure
        self.create_board()

        # populating board
        self.Read_Images()
        self.Add_pieces()

    def Add_labels(self):
        # Adding row labels to the board
        l=[]
        f=0
        if self.my_color == "white":
            l = list(range(8, 0, -1))
            f = self.label_frame1
        else:
            l = list(range(1, 9, 1))
            f = self.label_frame3

        pos = self.label_width + int(self.square_size / 2)
        for i in l:
            label_temp = Label(f, text=str(i), bg=self.label_frame_color, font=("Helvetica", 16),
                               fg="black")
            label_temp.place(anchor=CENTER, relx=0.5, y=pos)
            pos += self.square_size

        # Adding column labels
        if self.my_color == "white":
            l = ["A", "B", "C", "D", "E", "F", "G", "H"]
            f = self.label_frame4
        else:
            l = ["H", "G", "F", "E", "D", "C", "B", "A"]
            f = self.label_frame2
        pos = int(self.square_size / 2)
        for i in l:
            label_temp = Label(f, text=i, bg=self.label_frame_color, font=("Helvetica", 16), fg="black")
            label_temp.place(anchor=CENTER, rely=0.5, x=pos)
            pos += self.square_size

    def create_board(self):
        for i in range(0, 8):
            self.cells_canvases.append([])
            for j in range(0, 8):
                color = self.even_color if ((i + j) % 2) else self.odd_color
                c = Canvas(self.board_frame, width=self.square_size, height=self.square_size, bg=color,
                           highlightthickness=0)
                c.grid(row=i, column=j)
                self.cells_canvases[i].append(c)

    def run(self):
        self.window.mainloop()

    def Read_Images(self):
        image_path = "C:\\Users\\amram\PycharmProjects\\untitled\img\\black\\"
        image_names = ["b", "k", "n", "p", "q", "r"]

        for name in image_names:
            file = PhotoImage(file=(image_path + name + ".png"))
            self.Image_files[name] = file

        image_path = "C:\\Users\\amram\PycharmProjects\\untitled\img\\white\\"
        image_names = ["B", "K", "N", "P", "Q", "R"]

        for name in image_names:
            file = PhotoImage(file=(image_path + name + ".png"))
            self.Image_files[name] = file

    def Add_pieces(self):
        FEN_rows = self.FEN.split('/')

        i = 0
        j = 0
        if self.my_color == "white":
            for FEN_row in FEN_rows:
                for c in FEN_row:
                    if ord(c)>48 and ord(c) < 57:
                        j += int(c)
                    else:
                        Image = self.cells_canvases[i][j].create_image(int(self.square_size / 2), int(self.square_size / 2),
                              anchor=CENTER, image=self.Image_files[c])
                        self.cells_pieces[i][j]["ImgObj"] = Image
                        self.cells_pieces[i][j]["type"] = c

                        j += 1

                    i += 1 if j==8 else 0
                    j %= 8
        else:
            i = 7
            j = 7
            for FEN_row in FEN_rows:
                FEN_row = FEN_row[::-1]
                for c in FEN_row:
                    if ord(c) > 48 and ord(c) < 57:
                        j -= int(c)
                    else:
                        Image = self.cells_canvases[i][j].create_image(int(self.square_size / 2), int(self.square_size / 2),
                             anchor=CENTER, image=self.Image_files[c])
                        self.cells_pieces[i][j]["type"] = c
                        self.cells_pieces[i][j]["ImgObj"] = Image
                        j -= 1
                    i -= 1 if j==-1 else 0
                    j = 7 if j==-1 else j

    def trans(self, location):
        row = 8 - int(location[0])
        col = ord(location[1]) - 65
        if self.my_color == "white":
            return row, col
        else:
            return 7 - row, 7 - col

    def Delete_piece(self, loc):
        x, y = self.trans(loc)
        piece = self.cells_pieces[x][y]
        self.cells_canvases[x][y].delete(piece["ImgObj"])
        self.cells_pieces[x][y]["ImgObj"] = None
        self.cells_pieces[x][y]["type"] = ""

    def Add_piece(self, type, loc):
        self.Delete_piece(loc)
        x, y = self.trans(loc)
        Image = self.cells_canvases[x][y].create_image(int(self.square_size / 2), int(self.square_size / 2),
                  anchor=CENTER, image=self.Image_files[type])
        self.cells_pieces[x][y]["ImgObj"] = Image
        self.cells_pieces[x][y]["type"] = type

    def Move_piece(self, src_loc, dst_loc):
        #Delete piece at dst
        self.Delete_piece(dst_loc)
        #Move src to dst
        x, y = self.trans(src_loc)
        piece_type = self.cells_pieces[x][y]["type"]
        self.Delete_piece(src_loc)
        self.Add_piece(type=piece_type, loc=dst_loc)

    # use this function to print Win, lose , Draw at the end of the game
    def show_Msg(self, msg_str):
        self.msg.config(text=msg_str)
        self.msg.place(anchor=CENTER, relx=0.355, rely=0.5)

    def inc_Hmove(self):
        self.Hmove_count += 1
        self.Hmove_value_label.config(text=str(self.Hmove_count))

    def reset_Hmove(self):
        self.Hmove_count = 0
        self.Hmove_value_label.config(text=str(self.Hmove_count))

    def inc_Fmove(self):
        self.Hmove_count += 1
        self.Hmove_value_label.config(text=str(self.Hmove_count))



class Thread2(threading.Thread):
    def __init__(self, GUI_obj):
        threading.Thread.__init__(self)
        self.GUI = GUI_obj

    def run(self):
        time.sleep(2)
        # self.GUI.Delete_piece(1, 3)
        # self.GUI.f()
        self.GUI.reset_Hmove()
        self.GUI.inc_Fmove()
        self.GUI.Add_piece(type="q", loc="4E")
        self.GUI.Move_piece(src_loc="1G", dst_loc="7G")




# main program
FEN = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
G = GUI("white", FEN)

newThread = Thread2(G)
newThread.start()
G.window.mainloop()

print("finish")
