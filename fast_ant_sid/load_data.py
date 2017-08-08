
import glob
import numpy as np
import pandas as pd
import natsort


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

    ensemle_files = natsort.natsorted(glob.glob(rcp_path+"/*"))

    df_first = read_dp16_data(ensemle_files[0])

    df_mean_esl = pd.DataFrame(index=df_first.index,
                               columns=[em.split("/")[-1] for em in ensemle_files])

    for em in ensemle_files:

        em_name = em.split("/")[-1]
        df = read_dp16_data(em)
        df_mean_esl[em_name] = df["esl(m)"]

    return df_mean_esl



def read_magicc_output(fname):
    """
    This is a copy from the pymagicc package. Credits to Robert Giesecke.
    Input: Any MAGICC .OUT file
    Output: Pandas DataFrame
    """

    units = []
    with open(fname, 'r') as f:
        for idx,line in enumerate(f):
            if "YEARS" in line[0:10]:
                startidx = idx
            if "UNITS" in line[0:10]:
                unitidx = idx
                # keep out UNITS itself from the list
                units = line.split()[1:]
                # print units

    output = pd.read_csv(
        fname,
        engine='python',
        quotechar='"',
        sep='\s*',
        # quoting=csv.QUOTE_ALL,
        skipinitialspace=True,
        skiprows=startidx,
        index_col=0
    )

    # try to convert different units to one and the same
    if len(set(units)) > 1:
        units_to_numbers = {"Gt":1.e9,"Mt":1.e6,"kt":1.e3}
        conversion = [units_to_numbers[item[0:2]] for item in units]
        output = output * conversion

    return output

