import tkinter
from tkinter.simpledialog import askstring
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os



class Watermaking_UI:

    def __init__(self, images_path, lg_path, done_path):
        # setting paths and window
        self.images_path = images_path
        self.lg_path = lg_path
        self.done_path = done_path
        self.window = Tk()
        self.window.title("Image Watermaking Desktop App")
        self.window.minsize(width=1000, height=500)

        # setting variables that will be used in the code
        self.dragged_item = None
        self.drag_coords = 0, 0
        self.text = None
        self.sliders_size = None
        self.sliders_trans = None
        self.text_sliders_size = None
        self.prev_logo_0 = None
        self.prev_logo = None
        self.prev_logo_move = None
        self.prev_text = None
        self.cbaly = IntVar()
        self.cbaiy = IntVar()


        # creating checkboxes
        self.cb_add_logo_yes = Checkbutton(self.window, text='Are your images in the Images folder?', variable=self.cbaly, onvalue=1,
                                      offvalue=0, command=self.check_checkboxes)
        self.cb_add_logo_yes.place(x=50, y=450)
        self.cb_add_images_yes = Checkbutton(self.window, text='Is your logo in the Logo folder?', variable=self.cbaiy, onvalue=1,
                                        offvalue=0, command=self.check_checkboxes)
        self.cb_add_images_yes.place(x=50, y=420)

        self.window.mainloop()

    def reset(self):
        # destroying checkboxes
        self.cb_add_logo_yes.destroy()
        self.cb_add_images_yes.destroy()

        # change the name of the set up button and adding the logo and text button
        self.bt_setup.configure(text='RESET')
        self.bt_text = Button(text="Add text", command=self.add_text)
        self.bt_text.place(x=340, y=10, height=20, width=100)
        self.bt_logo = Button(text="Add logo", command=self.add_logo)
        self.bt_logo.place(x=560, y=10, height=20, width=100)

        # getting the first image to be used as an example
        all_images = os.listdir(self.images_path)
        self.prev_image = Image.open(self.images_path + all_images[0])
        self.prev_image = self.prev_image.resize((700, 350))
        self.tk_prev_image = ImageTk.PhotoImage(self.prev_image)
        self.canvas = Canvas(self.window, width=700, height=350)
        self.tk_prev_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_prev_image)
        self.canvas.place(x=150, y=55)

        # creating the watermark button
        self.bt_watermarking = Button(text="WATERMARK!", command=self.watermarking)
        self.bt_watermarking.place(x=450, y=450, height=40, width=100)

        # creating sliders to use as input for logo and text
        self.sliders_size = Scale(self.window, from_=1, to=100, orient=HORIZONTAL)
        self.sliders_size.place(x=870, y=450)
        self.sliders_size_text = Label(self.window, text="Logo's size (%)")
        self.sliders_size_text.place(x=870, y=430)

        self.sliders_trans = Scale(self.window, from_=0, to=100, orient=HORIZONTAL)
        self.sliders_trans.place(x=700, y=450)
        self.sliders_trans_text = Label(self.window, text="Logo's transparency (%)")
        self.sliders_trans_text.place(x=700, y=430)

        self.text_sliders_size = Scale(self.window, from_=1, to=100, orient=HORIZONTAL)
        self.text_sliders_size.place(x=50, y=450)
        self.text_sliders_size_text = Label(self.window, text="Font's size")
        self.text_sliders_size_text.place(x=50, y=430)

    def watermarking(self):
        # math part to get the coordinates and make it relative to the image
        x_logo = (self.canvas.coords(self.prev_logo_move))[0]/700
        y_logo = (self.canvas.coords(self.prev_logo_move))[1]/350
        x_text = (self.canvas.coords(self.text))[0]/700
        y_text = (self.canvas.coords(self.text))[1]/350
        rel_logo_width = (self.prev_logo.width()/700)
        rel_logo_height = (self.prev_logo.height()/350)

        # getting the paths
        all_images = os.listdir(self.images_path)
        logo = os.listdir(self.lg_path)

        for image in all_images:
            im = Image.open(self.images_path+image)
            lg = Image.open(self.lg_path+logo[1])
            img = ImageTk.PhotoImage(im)

            # adding the text to the image
            image_editable = ImageDraw.Draw(im)
            font = ImageFont.truetype('/arial.ttf', int(round(self.text_sliders_size.get())/(350)*(img.height())))
            image_editable.text((x_text*img.width(), y_text*img.height()), self.prev_text, (255, 255, 255), font=font, anchor='mm')

            #math part
            wl = img.width()*rel_logo_width
            hl = img.height()*rel_logo_height
            l = int(round((x_logo*img.width()) - wl/2))
            u = int(round((y_logo*img.height()) - hl/2))


            # adding the logo to the image
            lg = lg.resize((int(round(img.width()*rel_logo_width)), int(round(img.height()*rel_logo_height))))
            im.paste(lg, (l, u), lg.convert("RGBA"))

            im.save(self.done_path+image, "JPEG")

        messagebox.showinfo(title="Done", message="All the images have been processed")

    def add_text(self):
        # box to get string as input
        self.prev_text = askstring('Text', "What text would you like to write?")
        self.drag_all()

        # adding the text in the example image
        self.text = self.canvas.create_text(350, 175, fill='WHITE', font=('arial', self.text_sliders_size.get()), text=self.prev_text, tag=('draggable', 'canvas_text'))


    def add_logo(self):
        # enabling the drag
        self.drag_all()

        # getting the logo, converting and painting it with white
        self.all_images = os.listdir(self.lg_path)
        self.prev_logo_0 = Image.open(self.lg_path + self.all_images[0])
        self.prev_logo = self.prev_logo_0.convert('RGBA')
        datas = self.prev_logo.getdata()
        newData = []
        for item in datas:
            if item[3] == 0:
                newData.append(item)
            else:

                newData.append((255, 255, 255, int(round((self.sliders_trans.get())/100*255))))
        self.prev_logo.putdata(newData)

        # saving the logo changed to use after in the watermarking process
        self.prev_logo.save(self.lg_path + self.all_images[0].split('.')[0] + '_001.png')

        # resizing the logo using what the person wants as input
        self.prev_logo = self.prev_logo.resize((self.prev_logo.width * (self.sliders_size.get()) // 100, self.prev_logo.height * (self.sliders_size.get()) // 100))


        # placing the logo in the image example
        self.prev_logo = ImageTk.PhotoImage(self.prev_logo)
        self.prev_logo_move = self.canvas.create_image(350, 175, image=self.prev_logo, tag=('draggable', 'canvas_logo'))

    def drag_all(self):
        # enabling the drag
        self.canvas.tag_bind('draggable', '<ButtonPress-1>', self.start_drag)
        self.canvas.tag_bind('draggable', '<ButtonRelease-1>', self.stop_drag)
        self.canvas.tag_bind('draggable', '<B1-Motion>', self.drag)

    # drag settings
    def drag(self, event):
        xc, yc = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        dx, dy = xc - self.drag_coords[0], yc - self.drag_coords[1]
        self.drag_coords = xc, yc
        self.canvas.move(self.dragged_item, dx, dy)

    def start_drag(self, event):
        result = self.canvas.find_withtag('current')
        if result:
            self.dragged_item = result[0]
            self.drag_coords = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        else:
            self.dragged_item = None

    def stop_drag(self, event):
        self.dragged_item = None

    # start of the process
    def check_checkboxes(self):
        if (self.cbaly.get() == 1) and (self.cbaiy.get() == 1):
            self.bt_setup = Button(text="Set Up", command=self.reset)
            self.bt_setup.place(x=450, y=10, height=20, width=100)

        else:
            messagebox.showinfo(message="Please take a look at the checkboxes.")

