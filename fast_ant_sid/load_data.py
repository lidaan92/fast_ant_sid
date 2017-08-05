
import glob
import numpy as np
import pandas as pd
import dimarray as da
from scipy import interpolate


def running_mean(x, N):
    """ running mean with masked out boundaries, signal in beginning of array """
    # rmean = np.ma.array(x,copy=True,mask=True)
    rmean  = np.copy(x.values)
    rmean[:-N+1] = np.convolve(x, np.ones((N,))/N,"valid")
    rmean[-N+1:] = rmean[-N]
    return da.DimArray(rmean,axes=x.time,dims="time")


def load_ccsm4_data(scen="rcp26", relative_to=[1950,1980]):

    ccsm_file = "data/ccsm4_forcing/ccsm4_gmt_"+scen+".txt"
    ccsm_gmt_data = np.loadtxt(ccsm_file)
    end_of_first_ens_member = np.where(ccsm_gmt_data[:,0] == 2300)[0][0]
    time = ccsm_gmt_data[0:end_of_first_ens_member+1,0]
    gmt = ccsm_gmt_data[0:end_of_first_ens_member+1,1]
    f = interpolate.interp1d(time, gmt)
    yearly_time = np.arange(time[0],time[-1]+1,1)
    gmt = da.DimArray(f(yearly_time),axes=yearly_time,dims="time")
    gmt = gmt - gmt[relative_to[0]:relative_to[1]].mean()

    ## specific for DP16: prolong timeseries after 2175 with constant value
    ## of that year
    gmt_const = da.DimArray(np.repeat(gmt[2175],325),dims="time",
                  axes=np.arange(2176,2501))
    gmt = da.concatenate([gmt[1850:2175],gmt_const])

    return gmt


def read_dp16_data(fname):
    header = ["time", "weirun", "ro18", "sealev", "dtanta", "dtants", "dtantj",
        "dtseas", "rco2", "ecc", "obl", "prec", "facice", "facorb",
        "facco2", "toti(km3)", "totig(km3)", "totif(km3)", "tota(km2)",
        "totag(km2)", "totaf(km2)", "h(m)", "eofe(m)", "eofw(m)", "eof(m)",
        "esle(m)", "eslw(m)", "esl(m)"]

    df = pd.read_csv(fname,delimiter=r"\s+", header=None, names=header, index_col=0)
    # update time axis to start in 1950
    df.index = df.index + 1950
    return df


def get_dp16_mean_esl(rcp_path):

    ensemle_files = sorted(glob.glob(rcp_path+"/*"))

    df_first = read_dp16_data(ensemle_files[0])

    df_mean_esl = pd.DataFrame(index=df_first.index,
                               columns=[em.split("/")[-1] for em in ensemle_files])

    for em in ensemle_files:

        em_name = em.split("/")[-1]
        df = read_dp16_data(em)
        df_mean_esl[em_name] = df["esl(m)"]

    return df_mean_esl