
import os
import collections
import mystic
import pandas as pd
import fast_ant_sid.fast_ant_sid as fas; reload(fas)
import fast_ant_sid.load_data as ld; reload(ld)


# options
# decide wether to take a global maximum ice volume
# to lose accross DP16 ensemble members, or have it per member.
custom_max_vol = False

temperature_sensitivity = fas.square

sid_sens, fastrate, temp0, temp_thresh = 5.e-5, 10., 2., 2.5
bounds = ((0.,1.e-3),(0.,100.),(0.,10.),(0.,10.))

# Deconto & Pollard 2016 RCP projection data and global mean
# temperature evolution from MAGICC for CCSM4
# make sure you have these. They do not come with the repository
# as they are not publicly available.

dp16_path = "data/deconto_pollard16/"

dp16_slr_mean = collections.OrderedDict()
for case in ["RCP26","RCP26PIT","RCP45","RCP45PIT","RCP85","RCP85PIT"]:
    # in mm
    dp16_slr_mean[case] = ld.get_dp16_mean_esl(os.path.join(dp16_path,case))*1.e3

magicc_data_path = "data/magicc_gmts"
magicc_gmt = collections.OrderedDict()
for scen in ["RCP26","RCP45","RCP85"]:
    magicc_gmt[scen] = ld.read_magicc_output(
        magicc_data_path+"/DAT_SURFACE_TEMP_"+scen+".OUT")["GLOBAL"]

# determine maximum volume across all runs
max_volume_to_lose = dp16_slr_mean["RCP85PIT"].max().max()


def calibrate_ant_sid(max_volume_to_lose):

    parameters = (sid_sens, fastrate, temp0, temp_thresh)

    forcing = {scen:magicc_gmt[scen] for scen in magicc_gmt}

    parameters_ens = pd.DataFrame(columns=["sid_sens","fastrate","temp0","temp_thresh"])

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

        parameters = mystic.scipy_optimize.fmin(fas.least_square_error, parameters,
                          args=(forcing, reference_data, max_volume_to_lose,
                                temperature_sensitivity),
                          bounds=bounds, xtol = 1e-10, ftol = 1.e-10, maxiter = 10000, disp=0)

        parameters_ens.loc[member,:] = parameters

    return parameters_ens


if __name__ == "__main__":

    parameter_ens = calibrate_ant_sid(max_volume_to_lose)

    if not os.path.exists("data/parameters/"):
        os.makedirs("data/parameters/")

    parameter_ens.to_csv("data/parameters/parameter_ens.csv")