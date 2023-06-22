from PIL import Image
import os
import csv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def select_dir():
    image_extensions = [".jpg", ".png",]  # add additional image extensions if necessary.
    directory.set(filedialog.askdirectory())
    contents = [f for f in os.listdir(directory.get()) if any(f.endswith(e) for e in image_extensions)]
    contentsvar.set(contents)

root = Tk()
root.title("Logo Reformatting Tool")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

directory = StringVar()
directory_field = ttk.Entry(mainframe, width=20, textvariable=directory)
contents = []
contentsvar = StringVar(value=contents)


dir_button = ttk.Button(mainframe, text="Select Directory", command=select_dir).grid(column=1, row=1, sticky=W)
dir_label = ttk.Label(mainframe, textvariable=directory).grid(column=2, row=1, sticky=W, columnspan=2)
ttk.Label(mainframe, text="Folder Contents:").grid(column=1, row=2, sticky=W)
contents_listbox = Listbox(mainframe, height=10, listvariable=contentsvar, selectmode=EXTENDED)
contents_listbox.grid(column=1, row=3, columnspan=3)
scroller = ttk.Scrollbar(contents_listbox, orient=VERTICAL, command=contents_listbox.yview)
contents_listbox['yscrollcommand'] = scroller.set



root.mainloop()

input("Did it work?")


# os.chdir(r'L:\Ballinger Dept Resources\Computational Design and Data\Interiors Material Library Data Transfer\updated logos')


# print(f'Reformatting images in \n    {os.getcwd()}')
# try:
    # os.mkdir('reformat')
    # print("\ncreated directory 'reformat'")
# except FileExistsError:
    # print("\n'reformat' directory exists\n\n")


# image_data = []

# size = 100

# blank_img = Image.new('RGBA', (100,100), (255,255,255,0))

# ignored = []

# for file in os.listdir():
    # if file.lower().endswith(".jpg") or file.lower().endswith('.png'):
        # print(file)
        # image = Image.open(file)
        # width, height = image.size
        # ratio = size / max([width,height])
        # new_width = int(width * ratio)
        # new_height = int(height * ratio)
        # r = image.resize((new_width, new_height))
        # try:
            # r.save('resized/' + file)
        # except:
            # r = r.convert('RGB')
            # r.save('resized/' + file)

        # new_img = blank_img.copy()

        # place_x = int((size - new_width) / 2)
        # place_y = int((size - new_height) / 2)

        # new_img.paste(r, (place_x, place_y))

        # filename = file.split('.')[0] + '.png'

        # new_img.save('reformat/' + filename)
        # print(f'Image reformatted: {filename}')
    # else:
        # ignored.append(file)

# print('\n' + '-'*20 + '\n')
# for file in ignored:
    # print(f'File or Directory ignored: {file}')


# input("\nPress 'Enter' key to Exit")

# with open('image_data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for row in image_data:
#         writer.writerow(row)


