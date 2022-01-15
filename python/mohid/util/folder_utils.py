from pathlib import Path
import os


def create_model_folder_structure(yaml: dict, model: str):
    main_path = Path(yaml['MOHID_WATER']['MAIN_PATH'])
    model_path = main_path / model['PATH']
    if not os.path.isdir(main_path / "GeneralData/"):
        os.makedirs(main_path / "GeneralData/Bathymetry")
        os.makedirs(main_path / "GeneralData/BoundaryConditions")
        os.makedirs(main_path / "GeneralData/TimeSeries")
    if not os.path.isdir(model_path / "res/"):
        os.makedirs(model_path / "res/Run1/")
    if not os.path.isdir(model_path / "data/"):
        os.makedirs(model_path / "data/")
    if not os.path.isdir(model_path / "exe/"):
        os.makedirs(model_path / "exe/")
