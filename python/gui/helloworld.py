import tkinter
from tkinter import filedialog

main_path = None




def main():
    global main_path
    window = tkinter.Tk()
    window.title("ART Config Generator for MOHID")
    window.wm_attributes('-zoomed', 1)
    top_frame = tkinter.Frame(window).grid()
    main_path = tkinter.StringVar()

    mainpath_dir_lbl = tkinter.Label(top_frame, text="Main Path").grid(row=0, column=0)
    mainpath_dir_entry = tkinter.Entry(top_frame, textvariable=main_path).grid(row=0, column=1)
    mainpath_dir_btn = tkinter.Button(top_frame, text="Browse", command=browse_button).grid(row=0, column=2)

    mode_lbl = tkinter.Label(top_frame, text="Mode").grid(row=1, column=0)
    mode_menu = tkinter.Menu(top_frame)
    mode_list = {"Classic", "Forecast", "Hindcast"}
    mode_choice = tkinter.StringVar(top_frame)
    mode_choice.set("Forecast")
    mode_popup_menu = tkinter.OptionMenu(top_frame, mode_choice, *mode_list).grid(row=1, column=1)
    mode_choice.trace('w', change_dropdown(mode_choice))






    window.mainloop()


def browse_button():
    global main_path
    directory = filedialog.askdirectory()
    main_path.set(directory)
    print(directory)

def change_dropdown(var):
    print(var.get())


if __name__ == '__main__':
    main()
