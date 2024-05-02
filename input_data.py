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
    CIN_1 = 1
    CIN_2plus = 2
    DEATH = 3


# transition matrix
TRANS_MATRIX = [
    [0.947, 0.04, 0.01, 0.003],
    [0.6, 0.3, 0.097, 0.003],
    [0.2, 0.5, 0.297, 0.003],
    [0, 0, 0, 1]
]

# Annual state costs
ANNUAL_STATE_COST = [
    0,
    0,
    0,
    0]

# Cost of screening and colposcopy
HPV_TEST_COST = 35.09  # every 5 years
CO_TEST_COST = 69.25   # every 5 years
PAP_TEST_COST = 34.16  # every 3 years
COLPOSCOPY_COST = 155.0

# Natural death rate
NATURAL_DEATH_RATE = 0.003

# Update sensitivity and specificity parameters for each screening test
PAP_SENSITIVITY = 0.554
PAP_SPECIFICITY = 0.968

HPV_SENSITIVITY = 0.946
HPV_SPECIFICITY = 0.941

CO_TEST_SENSITIVITY = 0.994
CO_TEST_SPECIFICITY = 0.95


# Transition matrices for each screening strategy
def construct_transition_matrix(strategy):
    if strategy == "Pap":
        pap_transition_matrix = np.array([
            [0.947 * (1 - NATURAL_DEATH_RATE), 0.04, 0.01, 0.003 * (1 - PAP_SENSITIVITY)],
            [0.6, 0.3, 0.097, 0.003 * (1 - PAP_SENSITIVITY)],
            [0.2, 0.5, 0.297, 0.003 * (1 - PAP_SENSITIVITY)],
            [0, 0, 0, 1]
        ])
        return pap_transition_matrix

    elif strategy == "HPV":
        hpv_transition_matrix = np.array([
            [0.947 * (1 - NATURAL_DEATH_RATE), 0.04, 0.01, 0.003 * (1 - HPV_SENSITIVITY)],
            [0.6, 0.3, 0.097, 0.003 * (1 - HPV_SENSITIVITY)],
            [0.2, 0.5, 0.297, 0.003 * (1 - HPV_SENSITIVITY)],
            [0, 0, 0, 1]
        ])
        return hpv_transition_matrix

    elif strategy == "Co-test":
        co_test_transition_matrix = np.array([
            [0.947 * (1 - NATURAL_DEATH_RATE), 0.04, 0.01, 0.003 * (1 - CO_TEST_SENSITIVITY)],
            [0.6, 0.3, 0.097, 0.003 * (1 - CO_TEST_SENSITIVITY)],
            [0.2, 0.5, 0.297, 0.003 * (1 - CO_TEST_SENSITIVITY)],
            [0, 0, 0, 1]
        ])
        return co_test_transition_matrix
