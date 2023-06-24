import PIL.Image
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import math

APP_NAME = "Logo Processing Tool"
VERSION = "0.01 2023-06-24"
REPO = "https://github.com/bger-dhoward/logo-processor"

SHORT_PATH_LEN = 60  # truncate displayed directory paths if longer than this

def select_dir():
    global contents
    global contents_len
    global directory_path
    image_extensions = [".jpg", ".png", ]  # add additional image extensions if necessary.
    directory_path = filedialog.askdirectory()
    directory_display.set(shorten_path(directory_path, SHORT_PATH_LEN))
    contents = [f for f in os.listdir(directory_path) if any(f.lower().endswith(e) for e in image_extensions)]
    contents_len = len(contents)
    contentsvar.set(contents)


def shorten_path(path, max_len):
    separator = "..."
    if len(path) > max_len:
        half_len = math.floor((max_len - len(separator)) / 2)
        front = path[0:half_len]
        back = path[-half_len:]
        short_path = front + separator + back
        return short_path
    else:
        return path


def select_all():
    contents_listbox.selection_set(0, contents_len - 1)


def select_none():
    contents_listbox.selection_clear(0, contents_len - 1)


def help_about():
    msg = "Help:\nThis tool will resize selected .jpg and .png image files to the designated width and height " + \
          "using transparent pixels to pad the sides or top and bottom to maintain the appearance of the original " + \
          "aspect ratio.\n\nTo use, first select the directory (folder) where the original images exist, then " + \
          "select the available images in the list. Provide the final width and height dimensions (in pixels) " + \
          "then click the 'Reformat' button. By default, the reformatted images will be saved to a 'reformat' " + \
          "directory within the selected location (folder will be created if it does not already exist). To " + \
          "write the new image to the same directory, uncheck the box.\n\n(Note: since the tool saves the new " + \
          "image as a '.png' file, it may or may not overwrite the original image file if the box is unchecked)" + \
          "\n\n\nAbout:\nTool created by D. Howard using Python / Tkinter and prepared for distribution using " + \
          "pyinstaller.\n\n" + VERSION + "\n" + REPO
    messagebox.showinfo('Help / About', msg)


def reformat_images():
    print(final_width.get(), final_height.get())

    try:
        os.chdir(directory_path)
    except OSError:
        msg = "Click the 'Select Directory' button to navigate to the folder where " + \
              "your images are stored. Then select the images to be reformatted, and click " + \
              "the 'Reformat' button again."
        messagebox.showinfo("Select Directory", msg)
        print('OSError - skipping')
        return
    selected_images_idx = contents_listbox.curselection()
    if len(selected_images_idx) > 0:
        if save_to_reformat.get():
            try:
                os.mkdir('reformat')
            except FileExistsError:
                print('folder exists')
            path_prepend = 'reformat/'
        else:
            path_prepend = ''

        image_names = [contents[i] for i in selected_images_idx]

        for image_name in image_names:
            image = PIL.Image.open(image_name)
            width, height = image.size
            orig_ratio = width / height
            f_width = final_width.get()
            f_height = final_height.get()
            final_ratio = f_width / f_height

            if orig_ratio < final_ratio:
                scale = f_height / height
                # print("scale h")
            else:
                scale = f_width / width
                # print("scale w")
            scaled_height = math.floor(scale * height)
            scaled_width = math.floor(scale * width)
            scaled_orig_img = image.resize((scaled_width, scaled_height))

            # print(image_name, scale, scaled_width, scaled_height, scaled_orig_img.size)

            place_x = int((f_width - scaled_width) / 2)
            place_y = int((f_height - scaled_height) / 2)

            final_img = PIL.Image.new('RGBA', (f_width, f_height), (255, 255, 255, 0))
            final_img.paste(scaled_orig_img, (place_x, place_y))

            final_filename_path = path_prepend + image_name.split('.')[0] + '.png'

            final_img.save(final_filename_path)
        msg = f"{len(image_names)} images reformatted to size W:{f_width} x H:{f_height}."
        messagebox.showinfo('Images reformatted.', msg)
    else:
        print("no images selected")
        msg = "No images have been selected. Select one or more images, then try again."
        messagebox.showinfo("Empty Selection.", msg)


def quit_app():
    root.destroy()


root = Tk()
ttk.Style().theme_use('winnative')
root.title(APP_NAME)
root.geometry("400x425")
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(2, weight=1)

secondframe = ttk.Frame(root, padding="12 12 12 12")
secondframe.grid(column=0, row=1, sticky=(N, S, E, W))
secondframe.columnconfigure(5, weight=1)
secondframe.rowconfigure(3, weight=1)

directory_path = ""
directory_display = StringVar()
# directory_field = ttk.Entry(mainframe, width=50, textvariable=directory_display)
contents = []
contents_len = 0
contentsvar = StringVar(value=contents)

dir_button = ttk.Button(mainframe, text="Select Directory", command=select_dir)
dir_button.grid(column=0, row=1, sticky=W, )
dir_label = ttk.Label(mainframe, textvariable=directory_display)
dir_label.grid(column=0, row=2, sticky=W, columnspan=3,)
help_button = ttk.Button(mainframe, text="Help/About", command=help_about)
help_button.grid(column=2, row=1, columnspan=2, sticky=E)

sep1 = ttk.Separator(mainframe, orient=HORIZONTAL)
sep1.grid(column=0, row=3, columnspan=4, sticky=(E, W), pady=5)

ttk.Label(mainframe, text="Folder Contents:").grid(column=0, row=4, sticky=W)
contents_listbox = Listbox(mainframe, height=10, width=50,
                           listvariable=contentsvar, selectmode=EXTENDED, )
contents_listbox.grid(column=0, row=5, columnspan=3, sticky=(N, S, E, W))
scroller = ttk.Scrollbar(mainframe, orient=VERTICAL, command=contents_listbox.yview)
scroller.grid(column=3, row=5, stick=(N, S))
contents_listbox['yscrollcommand'] = scroller.set
select_all_button = ttk.Button(mainframe, text="Select All", command=select_all)
select_all_button.grid(column=0, row=6, sticky=W)
select_none_button = ttk.Button(mainframe, text="Select None", command=select_none)
select_none_button.grid(column=1, row=6, sticky=W)

sep2 = ttk.Separator(mainframe, orient=HORIZONTAL)
sep2.grid(column=0, row=7, columnspan=4, sticky=(E, W), pady=5)

final_width = IntVar(value=100)
final_height = IntVar(value=100)

ttk.Label(secondframe, text="Final Size:").grid(column=0, row=0, columnspan=2, sticky=W)
ttk.Label(secondframe, text="W:").grid(column=1, row=0, sticky=E)
final_width_entry = ttk.Entry(secondframe, textvariable=final_width, width=8)
final_width_entry.grid(column=2, row=0, sticky=(E, W))
ttk.Label(secondframe, text="H:").grid(column=3, row=0, sticky=W)
final_height_entry = ttk.Entry(secondframe, textvariable=final_height, width=8)
final_height_entry.grid(column=4, row=0, sticky=(E, W))

save_to_reformat = BooleanVar(value=True)
save_to_reformat_checkbox = ttk.Checkbutton(secondframe, variable=save_to_reformat, text="Save to 'reformat' folder?")
save_to_reformat_checkbox.grid(column=0, row=2, columnspan=4, sticky=W)

reformat_button = ttk.Button(secondframe, text="Reformat", command=reformat_images)
reformat_button.grid(column=0, row=4, sticky=W)
quit_button = ttk.Button(secondframe, text="Quit", command=quit_app)
quit_button.grid(column=5, row=4, sticky=E)

root.mainloop()
