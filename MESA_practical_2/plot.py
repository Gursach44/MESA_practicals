import mesa_reader as mr
import matplotlib.pyplot as plt


# specify variables corresponding to chosen mla values
mla_vals = [1, 2, 4]
dirs = [f"mla_{mla_val}_star/LOGS" for mla_val in mla_vals]
colors = ["blue", "orange", "green"]
markers = ["o", "s", "D"]  # for line endpoints

# initialize plot
plt.figure()

# create HR diagram
for i in range(len(mla_vals)):
    # read in history 
    logs = mr.MesaLogDir(dirs[i])
    history = logs.history

    # plot HR path
    plt.plot(history.log_Teff, history.log_L, color=colors[i], label=f"mla={mla_vals[i]}", alpha=1, lw=1)
    
    # plot end point
    plt.scatter(history.log_Teff[-1], history.log_L[-1], color=colors[i], s=(1+i)*30 - 20, zorder=10-i)

    # also print age of star at MS turnoff
    print(f"mla = {mla_vals[i]}, MS turnoff age = {history.star_age[-1]} yr")

# make plot spiffy and save
plt.xlabel(r"$\log_{10}(T_{\mathrm{eff}}\ /\ \mathrm{[K]})$")
plt.ylabel(r"$\log_{10}(L / L_\odot)$")
plt.gca().invert_xaxis()
plt.legend()
plt.tight_layout()
plt.savefig(f"plots/HR.png")

# initialize plot
plt.figure()

# plot log P vs log rho
for i in range(len(mla_vals)):
    # read in history 
    logs = mr.MesaLogDir(dirs[i])
    history = logs.history

    # plot variables
    plt.plot(history.log_cntr_Rho, history.log_cntr_P, color=colors[i], label=f"mla={mla_vals[i]}", alpha=1, lw=1)
    
    # plot end point
    plt.scatter(history.log_cntr_Rho[-1], history.log_cntr_P[-1], color=colors[i], s=(1+i)*30 - 20, zorder=10-i)

# make plot spiffy and save
plt.xlabel(r"$\log_{10}(\rho_c\ / \ \mathrm{[g\ cm^{-3}]})$")
plt.ylabel(r"$\log_{10}(P_c\ / \ \mathrm{[dyne\ cm^{-2}]})$")
plt.legend()
plt.tight_layout()
plt.savefig(f"plots/p_vs_rho.png")

# initialize plot
plt.figure()

# plot log T vs log rho
for i in range(len(mla_vals)):
    # read in history 
    logs = mr.MesaLogDir(dirs[i])
    history = logs.history

    # plot variables
    plt.plot(history.log_cntr_Rho, history.log_cntr_T, color=colors[i], label=f"mla={mla_vals[i]}", alpha=1, lw=1)
    
    # plot end point
    plt.scatter(history.log_cntr_Rho[-1], history.log_cntr_T[-1], color=colors[i], s=(1+i)*30 - 20, zorder=10-i)

# make plot spiffy and save
plt.xlabel(r"$\log_{10}(\rho_c\ / \ \mathrm{[g\ cm^{-3}]})$")
plt.ylabel(r"$\log_{10}(T_c\ / \ \mathrm{[K]})$")
plt.legend()
plt.tight_layout()
plt.savefig(f"plots/T_vs_rho.png")