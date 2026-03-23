import mesa_reader as mr
import numpy as np
from astropy.constants import M_sun
from scipy.integrate import quad
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.size'] = 12
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable


for profile_number in [1, 2, 3, 4, 5, 6]:
    # load in R and g-mode frequencies from mesa output
    # header row: _, m, logR, logT, logRho, logP, X, Y, Z, vel, cp, cs, pp, cno, tri_alpha, opac, _, brunt_N2, _, log_brunt_N, _, _, _
    mesa_data = np.loadtxt(f"lesson4/LOGS_gravity/profile{profile_number}.data", skiprows=6).T
    R = (10**mesa_data[2] * M_sun.cgs.value)[::-1]  # flip array to be increasing R
    brunt_N2 = mesa_data[17][::-1]  # flip array to match R

    # extract N from N^2, converting nans to zeros for following integration
    brunt_N = np.nan_to_num(np.sqrt(brunt_N2))

    # load in n and actual frequencies from GYRE output
    # header row: E_norm, M_star, R_star, Re(freq), Im(freq), l, n_pg, Re(omega), Im(omega)
    gyre_data = np.loadtxt(f"lesson4/gyre_out/gyre_summary{profile_number}.txt", skiprows=6).T
    period = (1. / gyre_data[3]) * 86400  # in seconds
    l = gyre_data[5]
    n_pg = gyre_data[6]

    # define a function to linearly interpolate N given an r
    brunt_N_interp = interp1d(R, brunt_N) 

    # define a function to be used by scipy.integrate.quad
    def Pi_0_integral(r):
        # first linearly interpolate to get an N value for this r
        N = brunt_N_interp(r)
        # return the integrand
        return N / r


    # integrate
    Pi_0 = -2.*np.pi**2. * (quad(Pi_0_integral, R[0], R[-1])[0])**(-1.)

    # compute Pi_nl
    Pi_nl = Pi_0 * n_pg / np.sqrt(l*(l+1))

    # plot Pi_nl against n, and period against n
    plt.plot(n_pg, Pi_nl, color='blue', linestyle='dashed', label='theoretical')
    plt.plot(n_pg, period, color='red', label='actual')
    plt.text(-30, np.median(period), rf"$\Delta \Pi_\text{{nl}} \approx {int(np.mean(np.diff(period)))}$ s", size=14)

    plt.title(f'$g$-mode Periods (Profile {profile_number})')
    plt.xlabel(r'$n_\text{pg}$')
    plt.ylabel('Period [s]')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"lesson4/gyre_out/g_modes_{profile_number}.png")
    plt.cla()