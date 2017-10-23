
import os
import collections
import mystic
import pandas as pd
import fast_ant_sid.fast_ant_sid as fas; reload(fas)
import fast_ant_sid.load_data as ld; reload(ld)


# options:

# Decide wether to take one global maximum ice loss volume or
# member specific global maximum ice loss volumes to constrain the parameterization.
custom_max_vol = False

# choose functional form of parameterization (linear or square)
temperature_sensitivity = fas.square

# define start values and bounds for the calibration parameters
sid_sens, fastrate, temp0, temp_thresh = 1.e-5, 20, 4., 4.
bounds = ((0.,1.e-3),(0.,100.),(0.,10.),(0.,10.))

# Deconto & Pollard (2016, Nature) reference data
# this data does not come with the repository as it is not publicly available.

dp16_path = "data/deconto_pollard16/"

dp16_slr_mean = collections.OrderedDict()
for case in ["RCP26","RCP26PIT","RCP45","RCP45PIT","RCP85","RCP85PIT"]:
    # in mm
    dp16_slr_mean[case] = ld.get_dp16_mean_esl(os.path.join(dp16_path,case))*1.e3

# GMT evolution from MAGICC for CCSM4 until year 2500.
magicc_data_path = "data/magicc_gmts"
magicc_gmt = collections.OrderedDict()
for scen in ["RCP26","RCP45","RCP85"]:
    magicc_gmt[scen] = ld.read_magicc_output(
        magicc_data_path+"/DAT_SURFACE_TEMP_"+scen+".OUT")["GLOBAL"]

# determine maximum volume across all runs
max_volume_to_lose = dp16_slr_mean["RCP85PIT"].max().max()

# run calibration
def calibrate_ant_sid(max_volume_to_lose):

    parameters = (sid_sens, fastrate, temp0, temp_thresh)

    forcing = {scen:magicc_gmt[scen] for scen in magicc_gmt}

    parameters_ens = pd.DataFrame(columns=["sid_sens","fastrate","temp0","temp_thresh"])
    remaining_errors = pd.DataFrame(columns=["remaining error"])

    for i,member in enumerate(dp16_slr_mean["RCP26PIT"].keys()[:]):

        print member,

        try:
            reference_data = {"RCP26":dp16_slr_mean["RCP26PIT"][member],
                              "RCP45":dp16_slr_mean["RCP45PIT"][member],
                              "RCP85":dp16_slr_mean["RCP85PIT"][member]}
        except KeyError:
            reference_data = {"RCP26":dp16_slr_mean["RCP26PIT"][member],
                              "RCP85":dp16_slr_mean["RCP85PIT"][member]}

        if custom_max_vol:
            max_volume_to_lose = dp16_slr_mean["RCP85PIT"][member].max()

        solution = mystic.scipy_optimize.fmin(fas.least_square_error, parameters,
                          args=(forcing, reference_data, max_volume_to_lose,
                                temperature_sensitivity),
                          bounds=bounds, xtol = 1e-10, ftol = 1.e-10, maxiter = 10000,
                          full_output=1, disp=0)

        parameters = solution[0]
        parameters_ens.loc[member,:] = parameters
        remaining_errors.loc[member] = solution[1]

    return parameters_ens, remaining_errors


if __name__ == "__main__":

    parameter_ens, remaining_errors = calibrate_ant_sid(max_volume_to_lose)

    if not os.path.exists("data/parameters/"):
        os.makedirs("data/parameters/")

    parameter_ens.to_csv("data/parameters/parameter_ens.csv")
    remaining_errors.to_csv("data/parameters/remaining_errors.csv")