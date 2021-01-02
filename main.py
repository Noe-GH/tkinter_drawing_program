import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
# pyscreenshot permite guardar lo que se muestra en pantalla en un objeto que puede ser manejado por la librería pillow.
import pyscreenshot


# Colors:
frame_menu_color = '#3b3b3b'
drawing_area_color = 'white'
color_palette = ('black', '#3b3b3b', 'gray', 'white', 'red', 'green', 'blue', 'purple', 'orange', 'cyan', 'light blue')
drawing_color = 'black'
menu_lbls_color = 'white'

# Drawing tools flags:
oval_brush = False
square_brush = False
line_brush = True
eraser_brush = False


def select_drawing_color(color):
    global drawing_color
    drawing_color = color


def activate_oval_brush():
    global oval_brush, square_brush, line_brush, eraser_brush
    oval_brush = True
    line_brush = False
    eraser_brush = False


def activate_line_brush():
    global oval_brush, square_brush, line_brush, eraser_brush
    oval_brush = False
    line_brush = True
    eraser_brush = False

def activate_eraser_brush():
    global oval_brush, square_brush, line_brush, eraser_brush
    oval_brush = False
    line_brush = False
    eraser_brush = True


class DrawEasy():

    def __init__(self):
        self.w = tk.Tk()
        self.w.title("Draw Easy")
        self.w.minsize(width=1280, height=720)
        self.w.resizable(0,0)

        self.img_line = tk.PhotoImage(file='icons/line.png')
        self.img_oval = tk.PhotoImage(file='icons/oval.png')
        self.img_eraser = tk.PhotoImage(file='icons/eraser.png')
        self.img_save = tk.PhotoImage(file='icons/save.png')
        self.img_square = tk.PhotoImage(file='icons/square.png')
        self.img_new = tk.PhotoImage(file='icons/new.png')

        # Widget creation Starts:
        self.frame_menu = tk.Frame(self.w, bg=frame_menu_color, height=50)
        self.lbl_text_color = tk.Label(self.frame_menu, text='  Colors:  ', fg=menu_lbls_color, bg=frame_menu_color)

        self.lbl_pick_color = tk.Label(self.frame_menu, text='  Pick a color:  ', fg=menu_lbls_color, bg=frame_menu_color)
        self.btn_pick_color = tk.Button(self.frame_menu, image=self.img_square, bd=0, command=self.color_picker)

        self.lbl_pen_size = tk.Label(self.frame_menu, text="  Pen size:  ", fg=menu_lbls_color, bg=frame_menu_color)
        self.spinb_pen_size = tk.Spinbox(self.frame_menu, from_=1, to=50)
        # Buttons
        self.lbl_brushes = tk.Label(self.frame_menu, text="  Brushes:  ", fg=menu_lbls_color, bg=frame_menu_color)
        self.btn_line = tk.Button(self.frame_menu, image=self.img_line, bd=0, command=activate_line_brush)
        self.btn_oval = tk.Button(self.frame_menu, image=self.img_oval, bd=0, command=activate_oval_brush)
        self.btn_eraser = tk.Button(self.frame_menu, image=self.img_eraser, bd=0, command=activate_eraser_brush)
        self.lbl_options = tk.Label(self.frame_menu, text="  Options:  ", fg=menu_lbls_color, bg=frame_menu_color)
        self.btn_save = tk.Button(self.frame_menu, image=self.img_save, bd=0, command=self.save_drawing)
        self.btn_new = tk.Button(self.frame_menu, image=self.img_new, bd=0, command=self.clear_cnv)

        self.cnv_area = tk.Canvas(self.w, bg=drawing_area_color, height=720)
        # Cuando se desea trabajar con eventos, es necesario usar bind.
        # Se pasa el nombre del evento en una tag.
        #   <B1-Motion> Es para usar el movimiento del mouse.
        # Se pasa como segundo argumento una función que recibe un evento.
        '''
        Lista de tags:
        | event                 | name                  |
        | Ctrl-c                | Control-c             |
        | Ctrl-/                | Control-slash         |
        | Ctrl-\                | Control-backslash     |
        | Ctrl+(Mouse Button-1) | Control-1             |
        | Ctrl-1                | Control-Key-1         |
        | Enter key             | Return                |
        |                       | Button-1              |
        |                       | ButtonRelease-1       |
        |                       | Home                  |
        |                       | Up, Down, Left, Right |
        |                       | Configure             |
        | window exposed        | Expose                |
        | mouse enters widget   | Enter                 |
        | mouse leaves widget   | Leave                 |
        |                       | Key                   |
        |                       | Tab                   |
        |                       | space                 |
        |                       | BackSpace             |
        |                       | KeyRelease-BackSpace  |
        | any key release       | KeyRelease            |
        | escape                | Escape                |
        |                       | F1                    |
        |                       | Alt-h                 |
        '''
        # Bindings
        self.cnv_area.bind("<B1-Motion>", self.draw)
        self.w.bind('<Control-F2>', self.clear_cnv)
        self.w.bind('<Control-s>', self.save_drawing)

        # Widget creation Ends.
        

        # Widget placing Starts:
        self.frame_menu.pack(fill='x')
        self.lbl_text_color.pack(side='left')
        for c in color_palette:
            self.btn_color = tk.Button(self.frame_menu, bg=c, width=3, height=2,
                command=lambda drawing_color = c : select_drawing_color(drawing_color)).pack(side='left')
        
        self.lbl_pick_color.pack(side='left')
        self.btn_pick_color.pack(side='left')
        
        self.lbl_pen_size.pack(side='left')
        self.spinb_pen_size.pack(side='left')

        # Buttons:
        self.lbl_brushes.pack(side='left')
        self.btn_line.pack(side='left')
        self.btn_oval.pack(side='left')
        self.btn_eraser.pack(side='left')
        self.lbl_options.pack(side='left')
        self.btn_save.pack(side='left')
        self.btn_new.pack(side='left')

        self.cnv_area.pack(fill='both')

        # Widget placing Ends.

        self.w.mainloop()

    def draw(self, event):
        '''
        Function that allows to draw in the canvas. It manages the type of drawing brush, its color and its size.
        '''
        x1, y1 = (event.x), (event.y)
        x2, y2 = (event.x), (event.y)
        if oval_brush:
            self.cnv_area.create_oval(x1, y1, x2, y2, fill=drawing_color, outline = drawing_color, width=self.spinb_pen_size.get())
        elif square_brush:
            self.cnv_area.create_rectangle(x1, y1, x2, y2, fill=drawing_color, outline = drawing_color, width=self.spinb_pen_size.get())
        elif line_brush:
            # Se restan y suman valores a las coordenadas para lograr el efecto. Cada vez que se oprime el botón izquierdo del mouse y se mueve el mouse, se crea una línea
            # que va desde las coordenadas del mouse -5 hasta las coordenadas del mouse +5.
            self.cnv_area.create_line(x1-5, y1-5, x2+5, y2+5, fill=drawing_color, width=self.spinb_pen_size.get())
        elif eraser_brush:
            self.cnv_area.create_oval(x1, y1, x2, y2, fill=drawing_area_color, outline = drawing_area_color, width=self.spinb_pen_size.get())
    
    # Poner event permite que se hagan atajos. Solo se pone event y nada más. Luego, se hace el binding en la ventana.
    def clear_cnv(self, event):
        '''
        Function that deletes everything on the canvas.
        '''
        self.cnv_area.delete("all")
    
    def save_drawing(self, event):
        '''
        Function that saves the content of the drawing area with a generic save window.
        '''
        # Se almacena en x1, y1 las coordenadas de la ventana más las cordenadas de donde comienza el canvas.
        x1 = self.w.winfo_rootx() + self.cnv_area.winfo_x() + 2
        y1 = self.w.winfo_rooty() + self.cnv_area.winfo_y() + 2

        # Se almacena en x2, y2 las coordenadas de la ventana más el tamaño del canvas.
        x2 = self.w.winfo_rootx() + self.cnv_area.winfo_width() - 2
        y2 = self.w.winfo_rootx() + self.cnv_area.winfo_height()

        # Los números que se suman y se restan son para que no aparezca un marco gris de la pantalla.

        # Función que crea una imagen de lo que se muestra en pantalla:
        img = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        try:
            with filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=[('.png', '*.png*'), ('.jpeg', '*.jpeg*')]) as mf:
                if mf:
                    img.save(mf.name, mf.name.split('/')[-1].split('.')[1])
        except AttributeError:
            pass
    
    def color_picker(self):
        # Función que permite utilizar un selector de colores ya prefabricado:
        color = colorchooser.askcolor()
        select_drawing_color(color[1])


app = DrawEasy()




