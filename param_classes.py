from enum import Enum
from input_data import *


class Tests(Enum):
    PAP_TEST = 0
    HPV_TEST = 1
    CO_TEST = 2


class Parameters:
    def __init__(self, test):

        # selected test
        self.test = test

        # initial health state
        self.initialHealthState = HealthStates.WELL

        # transition probability matrix of the selected test
        self.probMatrix = []

        # calculate transition probabilities depending on which therapy options is in use
        if test == Tests.PAP_TEST:
            self.probMatrix = construct_transition_matrix(strategy="Pap")
        elif test == Tests.HPV_TEST:
            self.probMatrix = construct_transition_matrix(strategy="HPV")
        elif test == Tests.CO_TEST:
            self.probMatrix = construct_transition_matrix(strategy="Co-test")

        # annual state costs and utilities
        self.annualStateCosts = ANNUAL_STATE_COST
        self.annualStateUtilities = ANNUAL_STATE_UTILITY

        # annual test cost
        if self.test == Tests.PAP_TEST:
            self.annualStateCosts[HealthStates.WELL.value] += PAP_TEST_COST / 3
            self.annualStateCosts[HealthStates.HPV.value] += COLPOSCOPY_COST / 3
            self.annualStateCosts[HealthStates.CIN_1.value] += COLPOSCOPY_COST / 3
            self.annualStateCosts[HealthStates.CIN_2.value] += COLPOSCOPY_COST / 3
            self.annualStateCosts[HealthStates.CIN_3.value] += COLPOSCOPY_COST / 3
        elif self.test == Tests.HPV_TEST:
            self.annualStateCosts[HealthStates.WELL.value] += HPV_TEST_COST / 5
            self.annualStateCosts[HealthStates.HPV.value] += COLPOSCOPY_COST / 5
            self.annualStateCosts[HealthStates.CIN_1.value] += COLPOSCOPY_COST / 5
            self.annualStateCosts[HealthStates.CIN_2.value] += COLPOSCOPY_COST / 5
            self.annualStateCosts[HealthStates.CIN_3.value] += COLPOSCOPY_COST / 5
        elif self.test == Tests.CO_TEST:
            self.annualStateCosts[HealthStates.WELL.value] += CO_TEST_COST / 5
            self.annualStateCosts[HealthStates.HPV.value] += COLPOSCOPY_COST / 5
            self.annualStateCosts[HealthStates.CIN_1.value] += COLPOSCOPY_COST / 5
            self.annualStateCosts[HealthStates.CIN_2.value] += COLPOSCOPY_COST / 5
            self.annualStateCosts[HealthStates.CIN_3.value] += COLPOSCOPY_COST / 5

        # discount rate
        self.discountRate = DISCOUNT


# Transition matrices for each screening strategy
def construct_transition_matrix(strategy):
    if strategy == "Pap":
        pap_transition_matrix = [
            [(1 - NATURAL_DEATH_RATE) * (1-PAP_TEST_POSITIVE), (1 - NATURAL_DEATH_RATE) * PAP_TEST_POSITIVE, 0, 0, 0, 0, NATURAL_DEATH_RATE],
            [(1-PAP_SENSITIVITY) * (1 - NATURAL_DEATH_RATE), 0.877*PAP_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.104*PAP_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.013*PAP_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.006*PAP_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0, NATURAL_DEATH_RATE],
            [0, 0.677*(1 - NATURAL_DEATH_RATE), 0.196*(1 - NATURAL_DEATH_RATE), 0.127*(1 - NATURAL_DEATH_RATE), 0, 0, NATURAL_DEATH_RATE],
            [0, 0, 0.213*(1 - NATURAL_DEATH_RATE), 0.4*(1 - NATURAL_DEATH_RATE), 0.387*(1 - NATURAL_DEATH_RATE), 0, NATURAL_DEATH_RATE],
            [0, 0, 0, 0.291*(1 - NATURAL_DEATH_RATE), 0.693*(1 - NATURAL_DEATH_RATE), 0.016*(1 - NATURAL_DEATH_RATE), NATURAL_DEATH_RATE],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ]
        return pap_transition_matrix

    elif strategy == "HPV":
        hpv_transition_matrix = [
            [(1 - NATURAL_DEATH_RATE) * (1-HPV_TEST_POSITIVE), (1 - NATURAL_DEATH_RATE) * HPV_TEST_POSITIVE, 0, 0, 0, 0, NATURAL_DEATH_RATE],
            [(1-HPV_SENSITIVITY) * (1 - NATURAL_DEATH_RATE), 0.877*HPV_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.104*HPV_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.013*HPV_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.006*HPV_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0, NATURAL_DEATH_RATE],
            [0, 0.677*(1 - NATURAL_DEATH_RATE), 0.196*(1 - NATURAL_DEATH_RATE), 0.127*(1 - NATURAL_DEATH_RATE), 0, 0, NATURAL_DEATH_RATE],
            [0, 0, 0.213*(1 - NATURAL_DEATH_RATE), 0.4*(1 - NATURAL_DEATH_RATE), 0.387*(1 - NATURAL_DEATH_RATE), 0, NATURAL_DEATH_RATE],
            [0, 0, 0, 0.291*(1 - NATURAL_DEATH_RATE), 0.693*(1 - NATURAL_DEATH_RATE), 0.016*(1 - NATURAL_DEATH_RATE), NATURAL_DEATH_RATE],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ]
        return hpv_transition_matrix

    elif strategy == "Co-test":
        co_test_transition_matrix = [
            [(1 - NATURAL_DEATH_RATE) * (1-CO_TEST_POSITIVE), (1 - NATURAL_DEATH_RATE) * CO_TEST_POSITIVE, 0, 0, 0, 0, NATURAL_DEATH_RATE],
            [(1-CO_TEST_SENSITIVITY) * (1 - NATURAL_DEATH_RATE), 0.877*CO_TEST_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.104*CO_TEST_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.013*CO_TEST_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0.006*CO_TEST_SENSITIVITY*(1 - NATURAL_DEATH_RATE), 0, NATURAL_DEATH_RATE],
            [0, 0.677*(1 - NATURAL_DEATH_RATE), 0.196*(1 - NATURAL_DEATH_RATE), 0.127*(1 - NATURAL_DEATH_RATE), 0, 0, NATURAL_DEATH_RATE],
            [0, 0, 0.213*(1 - NATURAL_DEATH_RATE), 0.4*(1 - NATURAL_DEATH_RATE), 0.387*(1 - NATURAL_DEATH_RATE), 0, NATURAL_DEATH_RATE],
            [0, 0, 0, 0.291*(1 - NATURAL_DEATH_RATE), 0.693*(1 - NATURAL_DEATH_RATE), 0.016*(1 - NATURAL_DEATH_RATE), NATURAL_DEATH_RATE],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ]
        return co_test_transition_matrix

