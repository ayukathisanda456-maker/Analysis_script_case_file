#Importing necessary libraries
import numpy as np
from pathlib import Path

#Creating some generalised functions,taken from Kokab 0_pp.py. #Loading the IDs of all the variables for a given iteration.
def load_ids(it, base="part", directory="."):
    """Load particle IDs for a given iteration."""
    fname_id = Path(directory) / f"{base}.{it}.id"
    with open(fname_id, "rb") as f:
        ims_npro = np.fromfile(f, dtype=np.int32, count=1)[0]
        ims_np_all = np.fromfile(f, dtype=np.int32, count=ims_npro)
        particle_ids = np.fromfile(f, dtype=np.int64)
        particle_ids = particle_ids.astype(int)
    return particle_ids

#Load additional variables for specific particles
def load_variable(it, var_index, base="part", directory="."):
    """Load one variable for a given iteration (x, y, z, etc.)."""
    fname = Path(directory) / f"{base}.{it}.{var_index}"
    with open(fname, "rb") as f:
        npro = np.fromfile(f, dtype=np.int32, count=1)[0]
        np_all = np.fromfile(f, dtype=np.int32, count=npro)
        data = np.fromfile(f, dtype=np.float64)
    return data

def print_combined(data, headings):
    """Print a 2D array as a table with clearly visible column headings."""
    if data.ndim != 2:
        raise ValueError("data must be a 2D array")
    if data.shape[1] != len(headings):
        raise ValueError(
            f"Expected {data.shape[1]} headings, got {len(headings)}"
        )

    rows = [[str(value) for value in row] for row in data]
    widths = [
        max(len(str(headings[i])), *(len(row[i]) for row in rows))
        for i in range(len(headings))
    ]

    print("\nCombined data:", flush=True)
    print(" | ".join(str(title).ljust(widths[i]) for i, title in enumerate(headings)), flush=True)
    print("-+-".join("-" * width for width in widths), flush=True)

    for row in rows:
        print(" | ".join(value.ljust(widths[i]) for i, value in enumerate(row)))

if __name__=="__main__":
    it = 0
    #Consider only initial case at 0.

    var_names = ["x", "y", "z", "u", "v", "w", "d2", "T", "a", "b", "k", "qv"] #The different variables
    #retrieved from the binary files

    

    #Load IDs
    ids = load_ids(it,directory='/Volumes/Elements/Thisanda/case 1')
    N = len(ids,)

    #Uses the function of LoadIDs to simply load the ID of the particles from the zeroth iteration.
    #N is the number of particles in the simulation, which is determined by the length of the IDs array.

    all_vars = []
    for i, name in enumerate(var_names, start=1):
        vals = load_variable(it, i,directory='/Volumes/Elements/Thisanda/case 1')
        if len(vals) != N:
            raise ValueError(f"Mismatch in var {name}: expected {N}, got {len(vals)}")
        all_vars.append(vals)

    # Combine into one big array: [ID, x, y, z, u, v, w, d2, T, a, b, k, qv]
    combined = np.column_stack((ids, *all_vars))

    headings = ["ID", *var_names]
    print_combined(combined, headings)

    #combined = np.column_stack((ids, *all_vars))[np.newaxis, :, :]
