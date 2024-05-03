from enum import Enum
import input_data as data


class Tests(Enum):
    PAP_TEST = 0
    HPV_TEST = 1
    CO_TEST = 2


class Parameters:
    def __init__(self, test):

        # selected test
        self.test = test

        # initial health state
        self.initialHealthState = data.HealthStates.WELL

        # transition probability matrix of the selected test
        self.probMatrix = data.TRANS_MATRIX

        # annual state costs and utilities
        self.annualStateCosts = data.ANNUAL_STATE_COST
        self.annualStateUtilities = data.ANNUAL_STATE_UTILITY

        # annual test cost
        if self.test == Tests.PAP_TEST:
            self.annualStateCosts[data.HealthStates.WELL.value] += data.PAP_TEST_COST / 3
            self.annualStateCosts[data.HealthStates.CIN_1.value] += data.COLPOSCOPY_COST / 3
            self.annualStateCosts[data.HealthStates.CIN_2plus.value] += data.COLPOSCOPY_COST / 3
        elif self.test == Tests.HPV_TEST:
            self.annualStateCosts[data.HealthStates.WELL.value] += data.HPV_TEST_COST / 5
            self.annualStateCosts[data.HealthStates.CIN_1.value] += data.COLPOSCOPY_COST / 5
            self.annualStateCosts[data.HealthStates.CIN_2plus.value] += data.COLPOSCOPY_COST / 5
        elif self.test == Tests.CO_TEST:
            self.annualStateCosts[data.HealthStates.WELL.value] += data.CO_TEST_COST / 5
            self.annualStateCosts[data.HealthStates.CIN_1.value] += data.COLPOSCOPY_COST / 5
            self.annualStateCosts[data.HealthStates.CIN_2plus.value] += data.COLPOSCOPY_COST / 5

        # discount rate
        self.discountRate = data.DISCOUNT
