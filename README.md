## Ice discharge parametrization for Antarctica

Find the code for the ice discharge parametrization as submitted
(Nauels et al. 2017) and its calibration here.

Please contact the authors if you would like to rerun the calibration,
as we cannot the reference data from Deconto & Pollard (Nature 2016) within this repository.

Please also have a look at [example notebooks](examples) for illustrative plots and
sensitivity tests.

### Usage

`python run_calibration.py`


### Examples

The quadratic temperature sensitivity as
it is used in the manuscript is [here](examples/fast_sid_quadratic.ipynb).

For comparison, the linear sensitivity to global mean temperature deviations
is discussed [here](examples/fast_sid_linear.ipynb).

We show the sensitivity of Antarctic discharge projections to artifically
constrained parameter ranges, leading to compensation by the other free parameters,
in [this notebook](examples/fast_sid_param_sensitvity.ipynb).

### Dependencies

numpy, pandas, mystic, natsort

### Fortran sea level code

We provide the Fortran code that is part of the revised MAGICC sea level module
[here](fortran/MAGICC_SLR_AIS_SID_component.f90). Please not that this is for reference and cannot be executed without MAGICC itself. MAGICC is not open source
and can therefore not be provided here.

### Authors

Matthias Mengel, Potsdam Institute for Climate Impact Research, Germany

Alexander Nauels, Australian-German Climate and Energy College, Australia

### Cite as

not yet.

### Platforms

The code should run under Linux and OSX. Some adaptions to the paths
would be needed to make it run under Windows.

### License

This code is licensed under GPLv3, see the LICENSE.txt. See the commit history for authors.
