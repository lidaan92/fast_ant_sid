## Ice discharge parametrization for Antarctica

Find the code for the ice discharge parametrization as submitted
(Nauels et al. 2017) and its calibration here.

Please contact the authors if you would like to rerun the calibration,
as we cannot provide the forcing global mean temperatures and the reference
data from Deconto & Pollard (Nature 2016) within this repository.

Please also have a look at `examples/deconto_pollard_discharge_param.ipynb`
for sample plots and test of different temperature sensitivies.

### Usage

`python run_calibration.py`

Reading in the parmeters sets from `data/parameters/` folder:
``` python
import pandas
pandas.read_csv("data/parameters/parameters_ens.csv",index_col=0)
```

### Dependencies

numpy, pandas, mystic, natsort


### Authors

Matthias Mengel, Potsdam Institute for Climate Impact Research, Germany

Alexander Nauels, Australian-German Climate and Energy College, Australia

### Cite as

not yet.

### License

This code is licensed under GPLv3, see the LICENSE.txt. See the commit history for authors.
