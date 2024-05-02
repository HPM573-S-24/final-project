from enum import Enum
import input_data as data


class Therapies(Enum):
    """ mono vs. combination therapy """
    PAP_TEST = 0
    HPV_TEST = 1
    CO_TEST = 2


class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = data.HealthStates.WELL

        # annual treatment cost
        if self.therapy == Therapies.PAP_TEST:
            self.annualTreatmentCost = data.PAP_TEST_COST
        elif self.therapy == Therapies.HPV_TEST:
            self.annualTreatmentCost = data.HPV_TEST_COST
        elif self.therapy == Therapies.CO_TEST:
            self.annualTreatmentCost = data.CO_TEST_COST

        # transition probability matrix of the selected therapy
        self.probMatrix = data.TRANS_MATRIX

        # annual state costs and utilities
        self.annualStateCosts = data.ANNUAL_STATE_COST

        # discount rate
        self.discountRate = data.DISCOUNT
