import numpy as np
from enum import Enum

# simulation settings
POP_SIZE = 10000  # cohort population size
SIM_TIME_STEPS = 40  # length of simulation (years)
ALPHA = 0.05  # significance level for calculating confidence intervals
DISCOUNT = 0.03  # annual discount rate


# HealthStates
class HealthStates(Enum):
    """ health states of patients with HIV """
    WELL = 0
    HPV = 1
    CIN_1 = 2
    CIN_2 = 3
    CIN_3 = 4
    CANCER = 5
    DEATH = 6


# Natural death rate
NATURAL_DEATH_RATE = 0.00613

# Update sensitivity and specificity parameters for each screening test
PAP_SENSITIVITY = 0.554
PAP_SPECIFICITY = 0.968

HPV_SENSITIVITY = 0.946
HPV_SPECIFICITY = 0.941

CO_TEST_SENSITIVITY = 0.994
CO_TEST_SPECIFICITY = 0.95

PAP_TEST_POSITIVE = 0.038/3
HPV_TEST_POSITIVE = 0.268/5
CO_TEST_POSITIVE = 0.4/5

# Annual state costs
ANNUAL_STATE_COST = [
    0,
    0,
    0,
    0,
    0,
    0,
    0]

ANNUAL_STATE_UTILITY = [
    1,
    0.95,
    0.7,
    0.6,
    0.5,
    0.3,
    0]

# Cost of screening and colposcopy
HPV_TEST_COST = 35.09  # every 5 years
CO_TEST_COST = 69.25  # every 5 years
PAP_TEST_COST = 34.16  # every 3 years
COLPOSCOPY_COST = 155.0


