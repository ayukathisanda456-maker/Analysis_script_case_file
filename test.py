

import matplotlib.pyplot as plt
from pathlib import Path
from config import DataConfig
from Profile_Manager import ProfileAverager,IDFile_Use
from Calculations import retrieve_wall_shear_velocity
from Profiling import ProfilePlotter


def main():

    configs = [
        DataConfig(data_dir=Path('/Volumes/Elements/Thisanda/case 1'),
                   first_file_no=100000,last_file_no=100000,number_of_steps=1,file_pattern="avg{file_no}.nc"),
        DataConfig(data_dir=Path('/Volumes/Elements/Thisanda/case 2'),
                   first_file_no=100000,last_file_no=100000,number_of_steps=1,file_pattern="avg{file_no}.nc"),
        DataConfig(data_dir=Path('/Volumes/Elements/Thisanda/case 3'),
                   first_file_no=100000, last_file_no=100000, number_of_steps=1, file_pattern="avg{file_no}.nc")
    ]

    fig, ax = plt.subplots()

    variables = ("y", "rU", "Rxx", "Ryy", "Rzz", "Rxy", "Tke")
    for i, config in enumerate(configs, start=1):
        averager = ProfileAverager(config.files())
        profiles = averager.average(variables)
        wsv = retrieve_wall_shear_velocity(profiles, mu=config.mu)

        plotter = ProfilePlotter(
            wsv=wsv, mu=config.mu, delta=config.delta,initial_diameter=0.2,ax=ax
        )
        plotter.plot_u_plus(
            y=profiles["y"],
            u=profiles["rU"],
            ax=ax,
            labels=[f"Case {i}"],
        )

    plt.show()



if __name__ == "__main__":
    main()





