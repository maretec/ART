import tkinter as tk
import tkcalendar
from tkinter import filedialog
from tkinter import ttk


class ArtGenApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("ART Config Generator")
        style = ttk.Style()
        style.theme_use('clam')
        container = tk.Frame(self)
        container.grid()
        self.frames = {}

        for F in (StartPage, NewCfg, MohidSettings, MohidMpiSettings, MohidOpenMpSettings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nswe")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        start_lbl = ttk.Label(self, text="Welcome to Automatic Running Tool's Configuration Generator")
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
        mainpath_dir_lbl.grid(row=0, column=0, sticky="W", padx=10, pady=5)
        mainpath_dir_entry = ttk.Entry(self, textvariable=self.main_path)
        mainpath_dir_entry.grid(row=0, column=1, sticky="W", padx=10, pady=5)
        mainpath_dir_btn = ttk.Button(self, text="Browse", command=lambda: browse_dir_button(self.main_path))
        mainpath_dir_btn.grid(row=0, column=2, sticky="W", padx=10, pady=5)

        mode_lbl = ttk.Label(self, text="Mode")
        mode_lbl.grid(row=1, column=0, sticky="W", padx=10, pady=5)
        self.mode_list = {"Classic", "Forecast", "Hindcast"}
        mode_choice = tk.StringVar()
        mode_choice.set("Forecast")
        mode_popup_menu = ttk.OptionMenu(self, mode_choice, next(iter(self.mode_list)), *self.mode_list)
        mode_popup_menu.grid(row=1, column=1, sticky="W", padx=10, pady=5)

        days_per_run_lbl = ttk.Label(self, text="Days per Run")
        days_per_run_lbl.grid(row=2, column=0, sticky="W", padx=10, pady=5)
        days_per_run_entry = ttk.Entry(self)
        days_per_run_entry.grid(row=2, column=1, sticky="W", padx=10, pady=5)

        ref_day_to_start_lbl = ttk.Label(self, text="Reference Day to Start")
        ref_day_to_start_lbl.grid(row=3, column=0, sticky="W", padx=10, pady=5)
        ref_day_to_start_entry = ttk.Entry(self)
        ref_day_to_start_entry.grid(row=3, column=1, sticky="W", padx=10, pady=5)

        num_of_runs_lbl = ttk.Label(self, text="Number of Runs")
        num_of_runs_lbl.grid(row=4, column=0, sticky="W", padx=10, pady=5)
        num_of_runs_entry = ttk.Entry(self)
        num_of_runs_entry.grid(row=4, column=1, sticky="W", padx=10, pady=5)

        self.run_pre_processing_bool = tk.BooleanVar()
        # run_pre_processing_lbl = ttk.Label(self, text="Pre-processing")
        run_pre_processing_cbox = ttk.Checkbutton(self, text="Pre-processing", variable=self.run_pre_processing_bool,
                                                  onvalue=True, offvalue=False)
        run_pre_processing_cbox.grid(row=5, column=0, sticky="W", padx=10, pady=5)
        self.run_post_processing_bool = tk.BooleanVar()
        run_post_processing_cbox = ttk.Checkbutton(self, text="Post-processing", variable=self.run_post_processing_bool,
                                                   onvalue=True, offvalue=False)
        run_post_processing_cbox.grid(row=6, column=0, sticky="W", padx=10, pady=5)

        start_date_lbl = ttk.Label(self, text="Start Date")
        start_date_lbl.grid(row=7, column=0, sticky="W", padx=10, pady=5)
        start_date_entry = tkcalendar.DateEntry(self, year=2019)
        start_date_entry.grid(row=7, column=1, sticky="W", padx=10, pady=5)

        end_date_lbl = ttk.Label(self, text="End Date")
        end_date_lbl.grid(row=8, column=0, sticky="W", padx=10, pady=5)
        end_date_entry = tkcalendar.DateEntry(self, year=2018)
        end_date_entry.grid(row=8, column=1, sticky="W", padx=10, pady=5)

        self.radio_var = tk.IntVar()

        mohid_radio_btn = ttk.Radiobutton(self, text="MOHID", variable=self.radio_var, value=1,
                                          command=self.radio_change)
        mohid_radio_btn.grid(row=9, column=0, sticky="W", padx=10, pady=5)
        ww3_radio_btn = ttk.Radiobutton(self, text="WaveWatch III", variable=self.radio_var, value=2,
                                        command=self.radio_change)
        ww3_radio_btn.grid(row=10, column=0, sticky="W", padx=10, pady=5)
        wrf_radio_btn = ttk.Radiobutton(self, text="WRF", variable=self.radio_var, value=3,
                                        command=self.radio_change)
        wrf_radio_btn.grid(row=11, column=0, sticky="W", padx=10, pady=5)

        next_btn = ttk.Button(self, text="Next", command=lambda: controller.show_frame(self.next_frame))
        next_btn.grid(row=12, column=30, sticky="W", padx=10, pady=10)


class MohidSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        mpi_btn = ttk.Button(self, text="MPI", command=lambda: controller.show_frame(MohidMpiSettings))
        mpi_btn.grid(row=1, column=1, sticky="NSWE", padx=50)
        openmp_btn = ttk.Button(self, text="OpenMP", command=lambda: controller.show_frame(MohidOpenMpSettings))
        openmp_btn.grid(row=1, column=2, sticky="NSWE", padx=50)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


class MohidMpiSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.mpi_exe_path = tk.StringVar()
        self.keep_decomposed_files = tk.BooleanVar()
        self.screen_output_to_file = tk.BooleanVar()
        self.screen_output_path = tk.StringVar()

        num_domains_lbl = ttk.Label(self, text="Number of Domains")
        num_domains_lbl.grid(row=0, column=0, sticky="W", padx=10, pady=5)
        num_domains_entry = ttk.Entry(self)
        num_domains_entry.grid(row=0, column=1, sticky="W", padx=10, pady=5)

        mpi_exe_path_dir_lbl = ttk.Label(self, text="Mohid Exe Path")
        mpi_exe_path_dir_lbl.grid(row=1, column=0, sticky="W", padx=10, pady=5)
        mpi_exe_path_dir_entry = ttk.Entry(self, textvariable=self.mpi_exe_path)
        mpi_exe_path_dir_entry.grid(row=1, column=1, sticky="W", padx=10, pady=5)
        mpi_exe_path_dir_btn = ttk.Button(self, text="Browse", command=lambda: browse_file_button(self.mpi_exe_path))
        mpi_exe_path_dir_btn.grid(row=1, column=2, sticky="W", padx=10, pady=5)

        mpi_keep_decomposed_files_cbox = ttk.Checkbutton(self, text="Keep Decomposed Files",
                                                         variable=self.keep_decomposed_files,
                                                         onvalue=True, offvalue=False)
        mpi_keep_decomposed_files_cbox.grid(row=2, column=0, sticky="W", padx=10, pady=5)

        mpi_joiner_version_lbl = ttk.Label(self, text="MPI Joiner Version")
        mpi_joiner_version_lbl.grid(row=3, column=0, sticky="W", padx=10, pady=5)
        mpi_joiner_version_entry = ttk.Entry(self)
        mpi_joiner_version_entry.grid(row=3, column=1, sticky="W", padx=10, pady=5)

        max_time_lbl = ttk.Label(self, text="Max Time")
        max_time_lbl.grid(row=4, column=0, sticky="W", padx=10, pady=5)
        max_time_entry = ttk.Entry(self)
        max_time_entry.grid(row=4, column=1, sticky="W", padx=10, pady=5)

        screen_output_to_file_cbox = ttk.Checkbutton(self, text="Screen Output to File",
                                                     variable=self.screen_output_to_file,
                                                     onvalue=True, offvalue=False)
        screen_output_to_file_cbox.grid(row=5, column=0, sticky="W", padx=10, pady=5)

        screen_output_path_lbl = ttk.Label(self, text="Screen Output Path")
        screen_output_path_lbl.grid(row=6, column=0, sticky="W", padx=10, pady=5)
        screen_output_path_entry = ttk.Entry(self, textvariable=self.screen_output_path)
        screen_output_path_entry.grid(row=6, column=1, sticky="W", padx=10, pady=5)
        screen_output_path_btn = ttk.Button(self, text="Browse", command=lambda: browse_dir_button(self.screen_output_path))
        screen_output_path_btn.grid(row=6, column=2, sticky="W", padx=10, pady=5)


class MohidOpenMpSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


def browse_dir_button(path):
    directory = filedialog.askdirectory()
    path.set(directory)
    print(directory)


def browse_file_button(path):
    file = filedialog.askopenfilename()
    path.set(file)
    print(file)


app = ArtGenApp()
app.mainloop()
