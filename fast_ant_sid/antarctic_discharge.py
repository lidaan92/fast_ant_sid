

def calc_solid_ice_discharge(forcing_temperature,voltotal,a,b,
                            temp_sensitivity=np.exp):

    """ solid ice discharge as used in Nauels et al. 2017 for the
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