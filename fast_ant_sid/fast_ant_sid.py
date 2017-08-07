import numpy as np


def square(arg):

    return np.sign(arg)*np.square(arg)


def calc_solid_ice_discharge(forcing_temperature, parameters, voltotal,
                                  temp_sensitivity=square):

    """ Solid ice discharge as used in Nauels et al. 2017, ERL, submitted.
    """

    sid_sens, fast_rate, temp0, temp_thresh = parameters

    def slow_discharge(volume, temperature, temp0, sid_sens):
        # positive rates lead to sea level rise
        return -1.*sid_sens*volume*temp_sensitivity(temperature-temp0)

    ## time spans forcing period
    time = np.arange(0,len(forcing_temperature),1)

    icesheet_vol = np.zeros_like(forcing_temperature)
    icesheet_vol[0] = voltotal
    slr_from_sid = np.zeros_like(forcing_temperature)

    # positive rates lead to sea level rise
    fast_sid = -1* fast_rate*np.array(forcing_temperature > temp_thresh,
                                      dtype = np.float)

    for t in time[0:-1]:
        sid_slow = slow_discharge(icesheet_vol[t], forcing_temperature[t],
                                   temp0, sid_sens)
        icesheet_vol[t+1] =  sid_slow + fast_sid[t] + icesheet_vol[t]
        slr_from_sid[t+1] = voltotal - icesheet_vol[t+1]

    return slr_from_sid



# def calc_solid_ice_discharge(forcing_temperature, parameters, final_volume,
#                               temp_sensitivity=square):

#     """ as used in Nauels et al. ERL 2017 (in revision) """

#     sid_sens, fastrate, temp0, temp_thresh = parameters
#     # keep sid_expsens fixed at 1 here: it is incorporated in sid_sens
#     sid_expsens = 1.
#     voltotal = final_volume

#     slow_sid = calc_slow_solid_ice_discharge(
#         forcing_temperature, voltotal, sid_sens, sid_expsens,
#         temp_sensitivity=temp_sensitivity)

# #     fast_sid = np.zeros_like(forcing_temperature)
#     fast_sid = fastrate*np.array(forcing_temperature > temp_thresh,
#                                     dtype = np.float)
# #     print fast_sid
#     return slow_sid + scipy.integrate.cumtrapz(fast_sid, initial=0)


def least_square_error(parameters, forcing, reference_data, max_volume_to_lose):

    """ handles several scenarios for one parameter set.
        We assume that there is one global maximum ice volume that can be lost
        (not dependent on parameter set.) """

    least_sq_error = np.zeros(len(reference_data.keys()))
    for i,scen in enumerate(reference_data.keys()):
        forc = forcing[scen]
        refdata = reference_data[scen]

        # least square error between slr and
        # we here assume all ice can be lost until last year of simulation
        # final_volume = refdata[2500]
        slr = calc_solid_ice_discharge(forc, parameters, max_volume_to_lose,
                                    temp_sensitivity=square)

        least_sq_error[i] = ((slr - refdata)**2.).sum()

    return least_sq_error.sum()


def calc_solid_ice_discharge_nauels_gmd(forcing_temperature,voltotal,a,b,
                            temp_sensitivity=np.exp):

    """ OLD: here for reference
    solid ice discharge as used in Nauels et al. 2017 for the
    Greenland solid ice discharge. Ice loss is exponentially dependent
    on the driving temperature in Nauels et al. 2017. """

    def discharge(volume, temperature, a, b):

        ds = - (a * volume * temp_sensitivity(b*temperature))
        return ds

    ## time spans forcing period
    time = np.arange(0,len(forcing_temperature),1)

    icesheet_vol = np.zeros_like(forcing_temperature)
    icesheet_vol[0] = voltotal
    solid_ice_discharge = np.zeros_like(forcing_temperature)
    slr = np.zeros_like(forcing_temperature)

    for t in time[0:-1]:
        ds = discharge(icesheet_vol[t], forcing_temperature[t], a, b)
        icesheet_vol[t+1] =  ds + icesheet_vol[t]
        solid_ice_discharge[t] = ds
        slr[t+1] = voltotal - icesheet_vol[t+1]

    return slr, solid_ice_discharge