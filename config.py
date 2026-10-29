#Importing necessary libraries
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass(frozen=True)
class DataConfig:
    data_dir: Path #Define the path to files
    first_file_no: int = 0 #First file number that can exist, maybe the lowest amount of particles
    last_file_no: int = 150000 #The file generated with the highest iteration
    number_of_steps: int = 16 #The number of numbers to be generated for correct retrieval
    file_pattern: str = "avg{file_no}.nc" #Pattern of files for  properties

    mu: float = 1.5e-5 #Global constants:Kinematic viscosity
    delta: float = 0.1 #Global constants:channel half width
    re_tau: float = 180 #Global constant - Reynolds number
    dt : float = 0.005 #Global constant finite time element

    def __post_init__(self):
        if self.number_of_steps < 1:
            raise ValueError("the number of steps must be at least 1")
        if self.last_file_no<self.first_file_no:
            raise ValueError("The last file of iterations must be greater than the first file")
        if self.mu<=0 or self.delta <=0:
            raise ValueError("mu and delta must be positive")

    def iteration_numbers(self):
        return tuple(np.linspace(
            self.first_file_no,
            self.last_file_no,
            self.number_of_steps,
            dtype=int,
        ))

    def files(self):
        return tuple(
            self.data_dir / self.file_pattern.format(file_no=it)
            for it in self.iteration_numbers()
        )


