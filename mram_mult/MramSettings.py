# MramSettings.py
# This file defines the parameters of MRAM cells.
# ---------------
# File dependecy:
# ---------------
# Lung-Yen Chen
# lungyenc@princeton.edu

import math

#### DEFINE THE PARAMETERS BELOW ####

RES_P_MEAN = 2115   # Mean of the resistance of MRAM cells in P state
RES_AP_MEAN = 4545  # Mean of the resistance of MRAM cell in ap state
RES_P_STD = 112     # Standard variation of the resistance of MRAM cells in P
RES_AP_STD = 241    # Standard variation of the resistance of MRAM cells in AP

########## DEFINITION END ###########


cpM = 1/RES_P_MEAN
capM = 1/RES_AP_MEAN
cpV = RES_P_STD * RES_P_STD * (cpM**4)
cpStd = math.sqrt(cpV)
capV = RES_AP_STD * RES_AP_STD * (capM**4)
capStd = math.sqrt(capV)
md = cpM - capM