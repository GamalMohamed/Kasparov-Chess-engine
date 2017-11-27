import threading
from tkinter import *
import time


class GUI:
    def __init__(self, my_color, fen, current_player, fm, hm):
        self.my_color = my_color
        self.FEN = fen
        self.current_player = current_player  # our team or the opponent team
        self.Fmove_count = fm
        self.Hmove_count = hm

        # Dimensions
        self.init_time = 0
        self.square_size = 70
        self.frame_width = 250
        self.label_width = 25
        self.window_width = self.square_size * 8 + self.frame_width + 2 * self.label_width
        self.window_height = self.square_size * 8 + 2 * self.label_width

        # Colors
        self.numbering_color = "#ffde81"
        self.circle_color = "gray"
        self.our_team_color = "yellow"
        self.opponent_color = "violet"
        self.even_color = "#d78500"
        self.odd_color = "#ffde81"
        self.label_frame_color = "#8e4200"
        self.side_frame_color = "#55FF00"

        # Data structure
        self.cells_canvases = []
        self.recommended_ids = []
        self.cells_pieces = [[{"type": "", "ImgObj": None} for j in range(8)] for i in range(8)]
        self.Image_files = {}

        # GUI Creation
        self.window = Tk()
        self.window.title("Chess Game")
        self.path = "C:\\Users\\amram\PycharmProjects\\untitled\\"
        self.window.iconbitmap(self.path + "img\logo.ico")
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

        #current turn player
        colors_to_draw_with = self.our_team_color if self.current_player == 1 else self.opponent_color
        self.data_canvas = Canvas(self.Frame1, width=self.frame_width, height=350, bg=self.our_team_color,
                                  highlightthickness=0)
        self.data_canvas.place(anchor=NE, x=self.frame_width, y=0)

        #create our team's logo
        self.teamlogo = PhotoImage(file=self.path + "img\logo3.png")
        self.teamlogo = self.teamlogo.subsample(4, 3)
        self.logo_obj = self.data_canvas.create_image(125, 50, anchor=CENTER, image=self.teamlogo, state=HIDDEN)

        #create opponent's logo
        self.data_canvas.config(bg=self.opponent_color)
        self.opp_logo_obj = self.data_canvas.create_text(123, 50, anchor=CENTER, text="Opponent", font=("Calibri", "40", "bold"))


        if self.current_player == 1:  #it's our team's turn
            self.data_canvas.itemconfig(self.logo_obj, state=NORMAL)
        else:
            self.data_canvas.itemconfig(self.opp_logo_obj, state=NORMAL)

        # constructing timer
        self.timer_label = Label(self.Frame1, text="0 : 0", font=("Helvetica", 30, "bold") , bg= colors_to_draw_with)
        self.timer_label.place(anchor=CENTER, relx=0.5, rely=0.21)

        # Adding counters
        x = 62
        y = 250
        r = 30
        self.data_canvas.create_oval(x-r, y-r, x+r, y+r, fill="gray", outline="gray")
        self.data_canvas.create_oval(self.frame_width/2 + x - r, y - r, self.frame_width/2 + x + r, y + r, fill="gray", outline="gray")


        self.Fmove_title = Label(self.Frame1, text="FM", font=("Helvetica", 15), bg=colors_to_draw_with)
        self.Fmove_title.place(anchor=CENTER, x=x, y=y-50)
        self.Fmove_value_label = Label(self.Frame1, text=str(self.Fmove_count), font=("Helvetica", 15), fg="white", bg="gray")
        self.Fmove_value_label.place(anchor=CENTER, x=x, y=y)


        self.Hmove_title = Label(self.Frame1, text="HM", font=("Helvetica", 15), bg=colors_to_draw_with)
        self.Hmove_title.place(anchor=CENTER, x=x + self.frame_width/2, y=y-50)
        self.Hmove_value_label = Label(self.Frame1, text=str(self.Hmove_count), font=("Helvetica", 15), fg="white" , bg="gray")
        self.Hmove_value_label.place(anchor=CENTER, x=x + self.frame_width/2, y=y)



        # win/lose/Draw msgs
        self.msg = Label(self.window, text="Draw", pady=30, padx=20, font=("Helvetica", 70, "bold"), bg="red")

        # adding the numbering frame around board
        self.Add_labels()

        # create board structure
        self.create_board()

        # populating board
        self.Read_Images()
        self.Add_pieces()

    def Add_labels(self):
        # Adding row labels to the board
        l = []
        f = 0
        if self.my_color == "white":
            l = list(range(8, 0, -1))
            f = self.label_frame1
        else:
            l = list(range(1, 9, 1))
            f = self.label_frame3

        pos = self.label_width + int(self.square_size / 2)
        for i in l:
            label_temp = Label(f, text=str(i), bg=self.label_frame_color, font=("Helvetica", 16),
                               fg=self.numbering_color)
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
            label_temp = Label(f, text=i, bg=self.label_frame_color, font=("Helvetica", 16), fg=self.numbering_color)
            label_temp.place(anchor=CENTER, rely=0.5, x=pos)
            pos += self.square_size

    def create_board(self):
        for i in range(0, 8):
            self.cells_canvases.append([])
            self.recommended_ids.append([])
            for j in range(0, 8):
                color = self.even_color if ((i + j) % 2) else self.odd_color
                c = Canvas(self.board_frame, width=self.square_size, height=self.square_size, bg=color,
                           highlightthickness=0)
                c.grid(row=i, column=j)
                self.cells_canvases[i].append(c)

                id = c.create_rectangle(0, 0, self.square_size - 1, self.square_size - 1, state=HIDDEN, width=7,
                                        outline="red")
                self.recommended_ids[i].append(id)

    def Read_Images(self):
        image_path = self.path + "img\\black\\"
        image_names = ["b", "k", "n", "p", "q", "r"]

        for name in image_names:
            file = PhotoImage(file=(image_path + name + ".png"))
            self.Image_files[name] = file

        image_path = self.path + "img\\white\\"
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
                    if ord(c) > 48 and ord(c) < 57:
                        j += int(c)
                    else:
                        Image = self.cells_canvases[i][j].create_image(int(self.square_size / 2),
                                                                       int(self.square_size / 2),
                                                                       anchor=CENTER, image=self.Image_files[c])
                        self.cells_pieces[i][j]["ImgObj"] = Image
                        self.cells_pieces[i][j]["type"] = c

                        j += 1

                    i += 1 if j == 8 else 0
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
                        Image = self.cells_canvases[i][j].create_image(int(self.square_size / 2),
                                                                       int(self.square_size / 2),
                                                                       anchor=CENTER, image=self.Image_files[c])
                        self.cells_pieces[i][j]["type"] = c
                        self.cells_pieces[i][j]["ImgObj"] = Image
                        j -= 1
                    i -= 1 if j == -1 else 0
                    j = 7 if j == -1 else j

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
        # Delete piece at dst
        self.Delete_piece(dst_loc)
        # Move src to dst
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

    def show_rec(self, locs):
        for loc in locs:
            x, y = self.trans(loc)
            self.cells_canvases[x][y].itemconfig(self.recommended_ids[x][y], state=NORMAL)

    def hide_rec(self, locs):
        for loc in locs:
            x, y = self.trans(loc)
            self.cells_canvases[x][y].itemconfig(self.recommended_ids[x][y], state=HIDDEN)

    def switch_turn(self):

        if self.current_player == 1:  #if the previous turn was our turn

            self.data_canvas.config(bg=self.opponent_color)
            self.timer_label.config(bg=self.opponent_color)
            self.Fmove_title.config(bg=self.opponent_color)
            self.Hmove_title.config(bg=self.opponent_color)
            self.data_canvas.itemconfig(self.logo_obj, state=HIDDEN)
            self.data_canvas.itemconfig(self.opp_logo_obj, state=NORMAL)

        else:
            self.data_canvas.config(bg=self.our_team_color)
            self.timer_label.config(bg=self.our_team_color)
            self.Fmove_title.config(bg=self.our_team_color)
            self.Hmove_title.config(bg=self.our_team_color)
            self.data_canvas.itemconfig(self.logo_obj, state=NORMAL)
            self.data_canvas.itemconfig(self.opp_logo_obj, state=HIDDEN)

        self.current_player = 3 - self.current_player   #it's either 1 or 2

    def reset_timer(self):
        self.init_time = time.clock()
        self.timer_label.config(text="0 : 0")

    def update_timer(self):
        t = time.clock()
        diff = t - self.init_time
        s = str(int(diff / 60)) + " : " + str(int(diff % 60))
        self.timer_label.config(text=s)



class TimerHandler(threading.Thread):
    def __init__(self, GUI_obj):
        threading.Thread.__init__(self)
        self.GUI = GUI_obj
        self.GUI.reset_timer()

    def run(self):
        cur_player = self.GUI.current_player
        while True:
            if cur_player == self.GUI.current_player:
                self.GUI.update_timer()
            else:
                self.GUI.reset_timer()
                cur_player = self.GUI.current_player
            time.sleep(1)



class Thread2(threading.Thread):
    def __init__(self, GUI_obj):
        threading.Thread.__init__(self)
        self.GUI = GUI_obj

    def run(self):
        time.sleep(2)
        self.GUI.Delete_piece("7D")
        self.GUI.reset_Hmove()
        self.GUI.inc_Fmove()
        self.GUI.Add_piece(type="q", loc="7H")
        self.GUI.Move_piece(src_loc="1G", dst_loc="7G")

        l = ["4E", "2D"]
        self.GUI.show_rec(l)

        time.sleep(2)
        self.GUI.hide_rec(l)
        time.sleep(1)
        self.GUI.Move_piece("7F", "3B")



# main program

# variables defining the initial state of the game
our_color = "white"   # white/black
FEN = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
player_to_start = 2   # indicates who will start the game our team or the opponent team, 2 means opponent will start
FM_count = 0          # initial value for the full move counter
HM_count = 0          # initial value for half move counter

G = GUI("white", FEN, player_to_start, FM_count, HM_count)

# starting processing and timer threads
processingThread = Thread2(G)
processingThread.start()
t_hndlr = TimerHandler(G)
t_hndlr.start()

# running the GUI window on the main thread(main program thread)
G.window.mainloop()  #blocking function

