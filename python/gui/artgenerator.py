import tkinter as tk
import tkcalendar
from tkinter import filedialog
from tkinter import ttk


class ArtGenApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("ART Config Generator for MOHID")
        style = ttk.Style()
        style.theme_use('clam')
        container = tk.Frame(self)
        container.grid()
        self.frames = {}

        for F in (StartPage, NewCfg, MohidSettings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        start_lbl = ttk.Label(self, text="Welcome to Automatic Running Tool's MOHID Configuration Generator")
        start_lbl.pack(pady=10, padx=10)

        newcfg_btn = ttk.Button(self, text="Create new configuration", command=lambda: controller.show_frame(NewCfg))
        newcfg_btn.pack()


class NewCfg(tk.Frame):

    def radio_change(self):
        print(self.radio_var.get())
        if self.radio_var.get() == 1:
            self.next_frame = MohidSettings

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.main_path = tk.StringVar()
        self.next_frame = None

        mainpath_dir_lbl = ttk.Label(self, text="Main Path")
        mainpath_dir_lbl.grid(row=0, column=0)
        mainpath_dir_entry = ttk.Entry(self, textvariable=self.main_path)
        mainpath_dir_entry.grid(row=0, column=1)
        mainpath_dir_btn = ttk.Button(self, text="Browse", command=lambda: browse_button(self.main_path))
        mainpath_dir_btn.grid(row=0, column=2)

        mode_lbl = ttk.Label(self, text="Mode")
        mode_lbl.grid(row=1, column=0)
        self.mode_list = {"Classic", "Forecast", "Hindcast"}
        mode_choice = tk.StringVar()
        mode_choice.set("Forecast")
        mode_popup_menu = ttk.OptionMenu(self, mode_choice, next(iter(self.mode_list)), *self.mode_list)
        mode_popup_menu.grid(row=1, column=1)

        days_per_run_lbl = ttk.Label(self, text="Days per Run")
        days_per_run_lbl.grid(row=2, column=0)
        days_per_run_entry = ttk.Entry(self)
        days_per_run_entry.grid(row=2, column=1)

        ref_day_to_start_lbl = ttk.Label(self, text="Reference Day to Start")
        ref_day_to_start_lbl.grid(row=3, column=0)
        ref_day_to_start_entry = ttk.Entry(self)
        ref_day_to_start_entry.grid(row=3, column=1)

        num_of_runs_lbl = ttk.Label(self, text="Number of Runs")
        num_of_runs_lbl.grid(row=4, column=0)
        num_of_runs_entry = ttk.Entry(self)
        num_of_runs_entry.grid(row=4, column=1)

        self.run_pre_processing_bool = tk.BooleanVar()
        # run_pre_processing_lbl = ttk.Label(self, text="Pre-processing")
        run_pre_processing_cbox = ttk.Checkbutton(self, text="Pre-processing", variable=self.run_pre_processing_bool,
                                                  onvalue=True, offvalue=False)
        run_pre_processing_cbox.grid(row=5, column=0)
        self.run_post_processing_bool = tk.BooleanVar()
        run_post_processing_cbox = ttk.Checkbutton(self, text="Post-processing", variable=self.run_post_processing_bool,
                                                   onvalue=True, offvalue=False)
        run_post_processing_cbox.grid(row=6, column=0)

        start_date_lbl = ttk.Label(self, text="Start Date")
        start_date_lbl.grid(row=7, column=0)
        start_date_entry = tkcalendar.DateEntry(self, year=2018)
        start_date_entry.grid(row=7, column=1)

        end_date_lbl = ttk.Label(self, text="End Date")
        end_date_lbl.grid(row=8, column=0)
        end_date_entry = tkcalendar.DateEntry(self, year=2018)
        end_date_entry.grid(row=8, column=1)

        self.radio_var = tk.IntVar()

        mohid_radio_btn = ttk.Radiobutton(self, text="MOHID", variable=self.radio_var, value=1,
                                          command=self.radio_change)
        mohid_radio_btn.grid(row=9, column=0)
        ww3_radio_btn = ttk.Radiobutton(self, text="WaveWatch III", variable=self.radio_var, value=2,
                                        command=self.radio_change)
        ww3_radio_btn.grid(row=10, column=0)
        wrf_radio_btn = ttk.Radiobutton(self, text="WRF", variable=self.radio_var, value=3,
                                        command=self.radio_change)
        wrf_radio_btn.grid(row=11, column=0)

        next_btn = ttk.Button(self, text="Next", command=lambda: controller.show_frame(self.next_frame))
        next_btn.grid(row=11, column=30)


class MohidSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.radio_var = tk.IntVar()

        mpi_radio_btn = ttk.Radiobutton(self, text="MPI", variable=self.radio_var, value=1)
        mpi_radio_btn.grid(row=0, column=0)
        openmp_radio_btn = ttk.Radiobutton(self, text="OpenMP", variable=self.radio_var, value=2)
        openmp_radio_btn.grid(row=1, column=0)


def browse_button(path):
    directory = filedialog.askdirectory()
    path.set(directory)
    print(directory)


app = ArtGenApp()
app.mainloop()
