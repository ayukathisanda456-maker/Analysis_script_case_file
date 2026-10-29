import matplotlib.pyplot as plt
import numpy as np
from matplotlib import use


class ProfilePlotter:
    def __init__(self, wsv, mu, delta,initial_diameter, ax=None, *, grid=True, xlim=None, ylim=None, figsize=(8, 6),font_family="Tahoma", base_size=14):
        if ax is None:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        else:
            self.ax = ax
            self.fig = ax.figure

        self.grid = grid
        self.xlim = xlim
        self.ylim = ylim

        self.wsv = wsv
        self.delta = delta
        self.mu = mu
        self.int_diameter = initial_diameter
        self.font_label = {'family': 'serif', 'size': 14, 'weight': 'bold'}
        self.tick_labels = {'family': 'serif', 'size': 10}

        #Apply global rcParams immediately upon instantiation for higher quality outputs
        plt.rcParams.update({
            "figure.dpi": 300,
            "font.family": font_family,
            "font.size": base_size,
            "axes.labelsize": base_size + 1,
            "axes.titlesize": base_size + 1,
            "xtick.labelsize": base_size - 1,
            "ytick.labelsize": base_size - 1,
            "legend.fontsize": base_size - 1,
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.5,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            "text.usetex": True,
        })

    # The method that plots the basic u profile
    def plot_u_plus(self, y, u, ax=None, labels=None):
        if ax is None:
            _, ax = plt.subplots()

        def as_profiles(data, name):
            if isinstance(data, np.ndarray):
                if data.ndim == 1:
                    return [data]
                if data.ndim == 2:
                    return list(data)
                raise ValueError(f"{name} must contain 1D profiles")

            values = list(data)
            if not values:
                raise ValueError(f"{name} must contain at least one profile")
            if all(np.isscalar(value) for value in values):
                return [np.asarray(values)]

            profiles = [np.asarray(value) for value in values]
            if any(profile.ndim != 1 for profile in profiles):
                raise ValueError(f"{name} must contain 1D profiles")
            return profiles

        y_profiles = as_profiles(y, "y")
        u_profiles = as_profiles(u, "u")

        if len(y_profiles) == 1 and len(u_profiles) > 1:
            y_profiles = y_profiles * len(u_profiles)
        elif len(y_profiles) != len(u_profiles):
            raise ValueError("Provide one y profile per u profile, or one shared y profile")

        if labels is not None and len(labels) != len(u_profiles):
            raise ValueError("Provide one label per case")

        for i, (y_case, u_case) in enumerate(zip(y_profiles, u_profiles)):
            if y_case.size != u_case.size:
                raise ValueError(
                    f"Case {i + 1}: y and u must have the same number of data points"
                )

            y_plus = y_case * self.wsv / self.mu
            u_plus = u_case / self.wsv
            positive_y = y_plus > 0

            label = labels[i] if labels is not None else None
            ax.semilogx(y_plus[positive_y], u_plus[positive_y], label=label)
            ax.spines[['top','right']].set_visible(False)
            ax.tick_params(direction='in',which='both')

        for label in ax.get_xticklabels():
            label.set_fontproperties(self.tick_labels)

        for label in ax.get_yticklabels():
            label.set_fontproperties(self.tick_labels)

        ax.set_xlabel(r"$y^+$",fontdict=self.font_label,usetex=True)
        ax.set_ylabel(r"$u^+$", fontdict=self.font_label,usetex=True)
        ax.grid(self.grid)

        if labels is not None:
            ax.legend()

        return ax

    def plot_u_v_w(self, y, Rxx, Ryy, Rzz, ax=None, plus=True):
        ax = self.ax if ax is None else ax

        if plus:
            y_plus = y * self.wsv / self.mu
            x_axis = y_plus
            ax.set_xlabel(r"$y^+$")
        else:
            y_delta = y / self.delta
            x_axis = y_delta
            ax.set_xlabel(r"$\frac{y}{\delta}$")

        ax.plot(x_axis, np.sqrt(Rxx), label="u")
        ax.plot(x_axis, np.sqrt(Ryy), label="v")
        ax.plot(x_axis, np.sqrt(Rzz), label="w")
        ax.set_ylabel('rms velocities')
        ax.grid(self.grid)
        ax.legend()

        return ax

    def plot_Rey_stress(self, y, Rey_stress, plus=False, ax=None):
        ax = self.ax if ax is None else ax

        if plus:
            y_plus = y * self.wsv / self.mu
            x_axis = y_plus
            ax.set_xlabel(r"$y^+$")
        else:
            y_delta = y / self.delta
            x_axis = y_delta
            ax.set_xlabel(r"$\frac{y}{\delta}$")

        y_axis = -1 * Rey_stress / self.wsv ** 2
        ax.plot(x_axis, y_axis, label="Rey")
        ax.set_ylabel(r"Reynold shear stress")
        ax.grid(self.grid)

        return ax

    def one_plot_profile_grid(self,profiles, x_variable, y_variable, rows, cols, labels=None):
        profiles = tuple(profiles)

        if not profiles:
            raise ValueError("At least one profile is required")
        if rows < 1 or cols < 1:
            raise ValueError("rows and cols must be at least 1")
        if rows * cols < len(profiles):
            raise ValueError("The grid does not have enough subplots")

        if labels is None:
            labels = [f"Input {i + 1}" for i in range(len(profiles))]
        elif len(labels) != len(profiles):
            raise ValueError("Provide one label per profile")

        fig,axes = plt.subplots(
            rows,cols,figsize=(6 * cols, 4 * rows),squeeze=False
        )

        for i, (profile, label) in enumerate(zip(profiles, labels)):
            if x_variable not in profile or y_variable not in profile:
                raise KeyError(
                    f"Each profile must contain {x_variable!r} and {y_variable!r}"
                )

            x = np.asarray(profile[x_variable]).squeeze()
            y = np.asarray(profile[y_variable]).squeeze()

            if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
                raise ValueError(
                    f"{label}: {x_variable!r} and {y_variable!r} "
                    "must be 1D arrays of equal length"
                )

            ax = axes.flat[i]
            ax.plot(x, y)
            ax.set_xlabel(x_variable)
            ax.set_ylabel(y_variable)
            ax.grid(self.grid)

            if self.xlim is not None:
                ax.set_xlim(self.xlim)
            if self.ylim is not None:
                ax.set_ylim(self.ylim)

        for ax in axes.flat[len(profiles):]:
            ax.set_visible(False)

        return fig, axes

    def particle_diameter_histogram(self,d2):
        #Extracting the diameter from the d2
        dp = np.sqrt(d2) - self.int_diameter





