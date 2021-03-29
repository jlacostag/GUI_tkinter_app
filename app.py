from tkinter import *
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo, display_textbox, display_icon, display_images, extract_images,  resize_image, copy_text, save_all, save_image

all_content = []
all_images = []
img_idx = [0]
displayed_img = []

root = Tk()
root.title("PDF Extract")
root.geometry('+%d+%d' % (250, 50))


def right_arrow(all_images, current_img, que_text):
    if img_idx[-1] < len(all_images) - 1:
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(new_img)
        displayed_img.append(current_img)
        que_text.set(
            "imagen " + str(img_idx[-1] + 1) + "de" + str(len(all_images)))
    elif img_idx == len(all_images)-1:
        print("Fuera de rango")
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()


def left_arrow(all_images, current_img, que_text):
    if img_idx[-1] >= 1:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(new_img)
        displayed_img.append(current_img)
        que_text.set(
            "imagen " + str(img_idx[-1] + 1) + "de" + str(len(all_images)))
    elif img_idx == len(all_images)-1:
        print("Fuera de rango")
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()


def copy_text(content):
    root.clipboard_clear()
    root.clipboard_append(content[-1])


def save_all(images):
    counter = 1
    for i in images:
        if i.mode != "RBG":
            i = i.convert("RGB")
        i.save("img" + str(counter) + ".png", format="png")
        counter += 1


def save_image(i):
    if i.mode != "RBG":
        i = i.convert("RGB")
    i.save("img.png", format="png")


# header area
header = Frame(root, width=800, height=175, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

# main content area
main_content = Frame(root, width=800, height=250, bg="#20bebe")
main_content.grid(columnspan=3, rowspan=2, row=4)


def open_file():

    for i in img_idx:
        img_idx.pop()
    img_idx.append(0)

    browse_text.set("cargando....")

    file = askopenfile(parent=root, mode="rb", filetypes=[
                       ("PDF file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()

        page_content = page_content.replace('\u2122', "'")

        if all_content:
            for i in all_content:
                all_content.pop()

        for i in range(0, len(all_images)):
            all_images.pop()

        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        all_content.append(page_content)

        images = extract_images(page)
        for img in images:
            all_images.append(img)

        selected_image = display_images(images[img_idx[-1]])
        displayed_img.append(selected_image)

        display_textbox(page_content, 4, 0, root)

        browse_text.set("Navegar")

        img_menu = Frame(root, width=800, height=60)
        img_menu.grid(columnspan=3, rowspan=1, row=2)

        que_text = StringVar()
        que_img = Label(root, textvariable=que_text)
        que_text.set(
            "Imagen   " + str(img_idx[-1] + 1) + "  de  " + str(len(all_images)))
        que_img.grid(row=2, column=1)

        display_icon('img/arrow_l.png', 2, 0, E,
                     lambda: left_arrow(all_images, selected_image, que_text))
        display_icon('img/arrow_r.png', 2, 2, W,
                     lambda: right_arrow(all_images, selected_image, que_text))

        save_img = Frame(root, width=800, height=60, bg="#c8c8c8")
        save_img.grid(columnspan=3, rowspan=1, row=3)

        copyText_btn = Button(root, text="Copiar texto", command=lambda: copy_text(
            all_content), height=1, width=15)
        saveAll_btn = Button(
            root, text="Todas las imagenes", command=lambda: save_all(
                all_images), height=1, width=15)
        save_btn = Button(root, text="Guardar imagen", command=lambda: save_image(
            all_images[img_idx[-1]]), height=1, width=15)

        copyText_btn.grid(row=3, column=0)
        saveAll_btn.grid(row=3, column=1)
        save_btn.grid(row=3, column=2)


display_logo('img/logo.png', 0, 0)

# instruction
instruction = Label(root, text="Selecciona un PDF", bg="white")
instruction.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

# browse
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda: open_file(
), bg="#20bebe", fg="white", height=1, width=15)
browse_text.set("Browse")
browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

root.mainloop()
