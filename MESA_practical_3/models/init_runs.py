import numpy as np
import shutil


# create array of masses (Msun) of stars to be simulated, and save it
masses = np.logspace(-1, np.log10(50), 100)
np.savetxt("masses.txt", masses)

# iterate over masses and create directory + custom inlist for each
for i, m in enumerate(masses):
    m_str = f"{m:.4f}"
    # create directory and copy in template directory
    try:
        shutil.copytree("template/", m_str)

        # read in template inlist
        with open(f"{m_str}/inlist_project", "r") as f:
            inlist_contents = f.read()

        # modify line that specifies total mass and rewrite inlist
        inlist_contents = inlist_contents.replace("MASS_PLACEHOLDER", m_str)
        # ADDED AFTER 1.3115 MSUN SIMULATION TO ENSURE SIMULATION COMPLETES IN A REASONABLE TIME
        if m > 1.32 and m < 2.04:
            inlist_contents = inlist_contents.replace("log_center_temp_upper_limit = 8d0", "log_center_temp_upper_limit = 7.5d0")
        # if m > 2.04:
        #     inlist_contents = inlist_contents.replace("log_center_temp_upper_limit = 8d0", "! log_center_temp_upper_limit = 8d0")
        #     inlist_contents = inlist_contents.replace("log_center_temp_upper_limit = 8d0", 
        #                                               "log_center_temp_upper_limit = 8d0\n\n" \
        #                                               "   ! stop when the center mass fraction of h1 drops below this limit\n" \
        #                                               "   xa_central_lower_limit_species(1) = 'h1'\n" \
        #                                               "   xa_central_lower_limit(1) = 1d-8" \
        #                                               "   ! stop when He burn phase begins\n" \
        #                                               "   stop_at_phase_He_Burn = .true.\n\n" \
        #                                               "   ! prevent timesteps being limited by dX/X fraction\n" \
        #                                               "   dX_div_X_limit = 1")
        if m > 2.04:
            inlist_contents = inlist_contents.replace("log_center_temp_upper_limit = 8d0", 
                                                      "log_center_temp_upper_limit = 8d0\n\n" \
                                                      "   ! prevent timesteps being limited by dX/X fraction\n" \
                                                      "   dX_div_X_limit = 1")
        
        with open(f"{m_str}/inlist_project", "w") as f:
            f.write(inlist_contents)
            
        f.close()
        
    except FileExistsError:
        print(f"Directory {m_str} already exists. Skipping.")

# create shell script to run MESA for each mass
f = open("run_mesa.sh", "w")
f.write("#!/bin/bash\n\n")

# iterate over masses and add MESA run commands to script
for i, m in enumerate(masses):
    m_str = f"{m:.4f}"
    f.write(f"cd {m_str}\n")
    f.write("./mk\n")
    f.write("./rn\n")
    f.write("cd ..\n\n")

f.close()