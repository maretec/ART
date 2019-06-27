import tkinter as tk
import tkcalendar
from tkinter import filedialog

main_path = None


def main():
    global main_path
    window = tk.Tk()
    window.title("ART Config Generator for MOHID")
    # window.wm_attributes('-zoomed', 1)
    top_frame = tk.Frame(window).grid()
    main_path = tk.StringVar()

    mainpath_dir_lbl = tk.Label(top_frame, text="Main Path").grid(row=0, column=0)
    mainpath_dir_entry = tk.Entry(top_frame, textvariable=main_path).grid(row=0, column=1)
    mainpath_dir_btn = tk.Button(top_frame, text="Browse", command=browse_button).grid(row=0, column=2)

    mode_lbl = tk.Label(top_frame, text="Mode").grid(row=1, column=0)
    mode_menu = tk.Menu(top_frame)
    mode_list = {"Classic", "Forecast", "Hindcast"}
    mode_choice = tk.StringVar(top_frame)
    mode_choice.set("Forecast")
    mode_popup_menu = tk.OptionMenu(top_frame, mode_choice, *mode_list).grid(row=1, column=1)
    mode_choice.trace('w', change_dropdown(mode_choice))

    days_per_run_lbl = tk.Label(top_frame, text="Days per Run").grid(row=2, column=0)
    days_per_run_entry = tk.Entry(top_frame).grid(row=2, column=1)

    ref_day_to_start_lbl = tk.Label(top_frame, text="Reference Day to Start").grid(row=3, column=0)
    ref_day_to_start_entry = tk.Entry(top_frame).grid(row=3, column=1)

    num_of_runs_lbl = tk.Label(top_frame, text="Number of Runs").grid(row=4, column=0)
    num_of_runs_entry = tk.Entry(top_frame).grid(row=4, column=1)

    run_pre_processing_bool = tk.BooleanVar()
    # run_pre_processing_lbl = tk.Label(top_frame, text="Pre-processing")
    run_pre_processing_cbox = tk.Checkbutton(top_frame, text="Pre-processing", variable=run_pre_processing_bool,
                                                  onvalue=True, offvalue=False).grid(row=5, column=0)
    run_post_processing_bool = tk.BooleanVar()
    run_post_processing_cbox = tk.Checkbutton(top_frame, text="Post-processing", variable=run_post_processing_bool,
                                                   onvalue=True, offvalue=False).grid(row=6, column=0)

    start_date_lbl = tk.Label(top_frame, text="Start Date").grid(row=7, column=0)
    start_date_entry = tkcalendar.DateEntry(top_frame, year=2018).grid(row=7, column=1)

    end_date_lbl = tk.Label(top_frame, text="End Date").grid(row=8, column=0)
    end_date_entry = tkcalendar.DateEntry(top_frame, year=2018).grid(row=8, column=1)

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
