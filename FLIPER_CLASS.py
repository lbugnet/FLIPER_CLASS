#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:17:00 2018

@author: Lisa Bugnet
@contact: lisa.bugnet@cea.fr
This code is the property of L. Bugnet (please see and cite Bugnet et al.,2019 in prep).

This python code is made for the classification of pulsators.

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

What you need:
- The power density spectrum of the star filtered with a 20 days high pass filter.
- The effective temperature of the star (from Mathur et al., 2017 for instance)
- The "ML_CLASSIFICATION_TESS_SIMU_training" and "ML_CLASSIFICATION_Kepler_sample_training" files containing the training of the Random Forests,
    to be dowload on GitHub (https://github.com/lbugnet/FLIPER_CLASS)

A calling example is reported at the end of the code.
"""

from astropy.io import fits
import numpy as np
import _pickle as cPickle
import os, os.path
from math import *
import pandas as pd


class FLIPER:
    def __init__(self):
        self.nom        =   "FliPer"
        self.fp07       =   []
        self.fp7        =   []
        self.fp20       =   []
        self.fp50       =   []

    def Fp(self, star_tab_psd_20, kepmag):
        """
        Compute FliPer value from 0.7, 7, 20, and 50 muHz to Nyquist with 20 days filtered data.
        """
        end         =   277# muHz
        noise       =   self.HIGH_NOISE(star_tab_psd)
        Fp07_val    =   self.REGION(star_tab_psd, 0.7, end) - noise
        Fp7_val     =   self.REGION(star_tab_psd, 7, end)   - noise
        Fp20_val    =   self.REGION(star_tab_psd, 20, end)  - noise
        Fp50_val    =   self.REGION(star_tab_psd, 50, end)  - noise

        self.fp07.append(Fp07_val)
        self.fp7.append(Fp7_val)
        self.fp20.append(Fp20_val)
        self.fp50.append(Fp50_val)
        return self

    def HIGH_NOISE(self, star_tab_psd):
        """
        Function that computes photon noise from last 100 bins of the spectra
        """
        data_arr_freq   =   star_tab_psd[:,0]
        data_arr_pow    =   star_tab_psd[:,1]
        siglower        =   np.mean(data_arr_pow[-20:])
        return siglower

    def REGION(self,star_tab_psd,inic,end):
        """
        Function that calculates the average power in a given frequency range on PSD
        """
        x       =   np.float64(star_tab_psd)[:,0]
        y       =   np.float64(star_tab_psd)[:,1]
        ys      =   y[np.where((x >= inic) & (x <= end))]
        average =   np.mean(ys)
        return average


class ML:
    def __init__(self):
        self.nom = "ML estimate"
        self.logg=[]

    def PREDICTION(self, F07, F7, F20, F50,  path_to_training_file):
        """
        Estimation of logg/numax with machine learning (training given by 'ML_CLASSIFICATION_Kepler_sample_training' or 'ML_CLASSIFICATION_TESS_SIMU_training' to be dowload in GitHub).
        """
        listing         =   {'lnF07': self.CONVERT_TO_LOG(F07), 'lnF7': self.CONVERT_TO_LOG(F7), 'lnF20': self.CONVERT_TO_LOG(F20), 'lnF50': self.CONVERT_TO_LOG(F50), 'teff': teff }
        df              =   pd.DataFrame(data=listing)
        columnsTitles   =   ['lnF07', 'lnF7', 'lnF20', 'lnF50', 'teff']
        df              =   df.reindex(columns=columnsTitles)
        X               =   df.values

        with open(path_to_training_file, 'rb') as f:
            rf  =   cPickle.load(f)

        class_predicted  =   rf.predict(X)
        self.logg.append(class_predicted)
        return class_predicted

    def CONVERT_TO_LOG(self, param):
        return np.log10(param)


"""
-------------------------------------------------------------------------------
 CALLING SEQUENCE
-------------------------------------------------------------------------------

ALL NEEDED INFORMATIONS:
"""
#Paths to PSD fits files computed from light curves filtered with 20 days
psd_path_20             =   '/???/???'

#Path to trained random forest (to be dowloaded on GitHub)
PATH_TO_TRAINING_FILE   =   '/???/ML_CLASSIFICATION_Kepler_sample_training'
#Give star parameters
teff            =   ???

"""
Calculate FliPer values.
"""
Fliper =   FLIPER().Fp(star_tab_psd) #data_arr_freq   =   star_tab_psd[:,0],        data_arr_pow    =   star_tab_psd[:,1]
Fp07        =   Fliper.fp07[0]
Fp7         =   Fliper.fp7[0]
Fp20        =   Fliper.fp20[0]
Fp50        =   Fliper.fp50[0]

"""
Estimation of surface gravity and/or numax from the training file ('/???/ML_CLASSIFICATION_Kepler_sample_training' for instance).
"""
class_predicted=ML().PREDICTION(Fp07, Fp7, Fp20, Fp50, teff, PATH_TO_TRAINING_FILE)
