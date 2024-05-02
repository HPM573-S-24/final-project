import deampy.econ_eval as econ
import deampy.statistics as stat
import numpy as np
from deampy.markov import MarkovJumpProcess
from deampy.plots.sample_paths import PrevalencePathBatchUpdate

from input_data import HealthStates


class Patient:
    def __init__(self, id, parameters):

        self.id = id
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=self.params)

    def simulate(self, n_time_steps):

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # Markov jump process
        markov_jump = MarkovJumpProcess(transition_prob_matrix=self.params.probMatrix)

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:
            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState    # assuming everyone starts in "Well"
        self.nPotentialCancer = 0
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time_step, new_state):

        if not self.get_if_alive():
            return

        if new_state == HealthStates.CIN_2plus:
            self.nPotentialCancer += 1

        self.costUtilityMonitor.update(t=time_step,
                                       current_state=self.currentState,
                                       next_state=new_state)
        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState in HealthStates.DEATH:
            return False
        else:
            return True


class PatientCostUtilityMonitor:
    def __init__(self, parameters):

        self.params = parameters
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, t, current_state, next_state):

        cost = 0.5 * (self.params.annualStateCosts[current_state.value] +
                      self.params.annualStateCosts[next_state.value])

        utility = 0.5 * (self.params.annualStateUtilities[current_state.value] +
                         self.params.annualStateUtilities[next_state.value])

        self.totalDiscountedCost += econ.pv_single_payment(payment=cost,
                                                           discount_rate=self.params.discountRate/2,
                                                           discount_period=2 * t+1)
        self.totalDiscountedUtility += econ.pv_single_payment(payment=utility,
                                                              discount_rate=self.params.discountRate/2,
                                                              discount_period=2 * t+1)


class Cohort:
    def __init__(self, id, pop_size, parameters):
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, n_time_steps):

        # populate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              parameters=self.params)
            # simulate
            patient.simulate(n_time_steps)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.nPotentialCancer = []
        self.costs = []
        self.utilities = []

        self.statCost = None
        self.statUtility = None
        self.statNumCancer = None

    def extract_outcome(self, simulated_patient):

        self.nPotentialCancer.append(simulated_patient.stateMonitor.nPotentialCancer)
        self.costs.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
        self.utilities.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        self.statCost = stat.SummaryStat(
            name='Discounted cost', data=self.costs)
        self.statUtility = stat.SummaryStat(
            name='Discounted utility', data=self.utilities)
        self.statNumCancer = stat.SummaryStat(
            name='Total Number of Potential Cancer Detected', data=self.nPotentialCancer)
