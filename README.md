# FLIPER CLASSIFICATION

author: Lisa Bugnet

contact: lisa.bugnet@cea.fr

This repository is the property of L. Bugnet (please see and cite Bugnet et al.,2019 in prep).

# Description of the files

The user should first use the FLIPER class to calculate FliPer values
from 0.7,7,20 and 50 muHz (see Bugnet et al.,2018)
(see CALLING SEQUENCE at the end of this code).
These values are the parameters needed by the machine learning Random Forest
(along with the effective temperature).

The Random Forest classifiers are already trained and stored in the
"ML_logg_training_paper" and "ML_numax_training_paper" files to estimate
logg or numax. They should be download on GitHub before running this code.
The estimation of surface gravity should be made by the use of the "ML" class
(see CALLING SEQUENCE at the end of this code).

# What you need:

- The power density spectrum of the star filtered with a 20 days high pass filter.
- The effective temperature of the star (from Mathur et al., 2017 for instance)
- The "ML_CLASSIFICATION_TESS_SIMU_training" and "ML_CLASSIFICATION_Kepler_sample_training" files containing the training of the Random Forests,
    to be dowload on GitHub (https://github.com/lbugnet/FLIPER_CLASS)


## CALLING SEQUENCE


ALL NEEDED INFORMATIONS:
```
#Paths to PSD fits files computed from light curves filtered with 20 days
psd_path_20             =   '/???/???'
```

Path to trained random forest (to be dowloaded on GitHub)
```
PATH_TO_TRAINING_FILE   =   '/???/ML_CLASSIFICATION_Kepler_sample_training'
```

Give star parameters
```
teff            =   ???
```

Calculate FliPer values.
```
Fliper =   FLIPER().Fp(star_tab_psd) #data_arr_freq   =   star_tab_psd[:,0],        data_arr_pow    =   star_tab_psd[:,1]
Fp07        =   Fliper.fp07[0]
Fp7         =   Fliper.fp7[0]
Fp20        =   Fliper.fp20[0]
Fp50        =   Fliper.fp50[0]
```

Estimation of surface gravity and/or numax from the training file ('/???/ML_CLASSIFICATION_Kepler_sample_training' for instance).
```
class_predicted=ML().PREDICTION(Fp07, Fp7, Fp20, Fp50, teff, PATH_TO_TRAINING_FILE)
```
