
import numpy as np
import xarray as xr

class ProfileAverager:
    def __init__(self,files):
        self.files = tuple(files)

    #Calculate the average
    def average(self,variable_names):
        variable_names = tuple(dict.fromkeys(variable_names))
        totals = {}

        if not self.files:
            raise ValueError("No input files were provided and taken")

        #Input files are open using xarray
        for path in self.files:
            with xr.open_dataset(path) as ds:
                #Looping through all variable names
                for name in variable_names:
                    #We loop through each individual variable in the file and maintain a dictionary for its values
                    if name not in ds:
                        raise KeyError(f"{name!r} is missing from {path}")

                    values = np.asarray(ds[name].values,dtype=float).squeeze()

                    if values.ndim!=1:
                        raise ValueError(f"{name!r} in {path} should be a 1D profile;"
                                         f"got shape {values.shape}")

                    if name not in totals:
                        #Returns an array of similar shape and type as a given array
                        totals[name] = np.zeros_like(values,dtype=float)
                    elif totals[name].shape != values.shape:
                        raise ValueError(f"{name!r} has inconsistent shapes across files")

                    #Sums all the variables individually(i.e.going through each variable at a time and totaling)
                    totals[name] +=values

        #Returns the name of the variable alongside its average across all the totals array
        return {name:total/len(self.files)
                for name,total in totals.items()}

class IDFile_Use:
    def __init__(self, config, base="part"):
        self.config = config
        self.base = base

    def extract_variable_ids(self, it):
        path = self.config.data_dir / f"{self.base}.{it}.id"
        with path.open("rb") as f:
            npro = np.fromfile(f, dtype=np.int32, count=1)
            if npro.size != 1:
                raise ValueError(f"Missing processor count in {path}")

            np.fromfile(f, dtype=np.int32, count=int(npro[0]))
            return np.fromfile(f, dtype=np.int64)

    def load_variable(self, it, var_index):
        path = self.config.data_dir / f"{self.base}.{it}.{var_index}"
        with path.open("rb") as f:
            npro = np.fromfile(f, dtype=np.int32, count=1)
            if npro.size != 1:
                raise ValueError(f"Missing processor count in {path}")

            np.fromfile(f, dtype=np.int32, count=int(npro[0]))
            return np.fromfile(f, dtype=np.float64)





