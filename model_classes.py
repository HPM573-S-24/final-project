import numpy as np
import deampy.econ_eval as econ
import deampy.statistics as stat
from deampy.markov import MarkovJumpProcess
from input_data import HealthStates


class Patient:
    def __init__(self, id, parameters):
        self.id = id
        self.params = parameters
        self.state_monitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, n_time_steps):
        rng = np.random.RandomState(seed=self.id)
        markov_jump = MarkovJumpProcess(transition_prob_matrix=self.params.probMatrix)

        k = 0
        while self.state_monitor.get_if_alive() and k < n_time_steps:
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.state_monitor.currentState.value,
                rng=rng)

            new_state = HealthStates(new_state_index)
            self.state_monitor.update(time_step=k, new_state=new_state)

            if new_state != HealthStates.WELL and new_state != HealthStates.DEATH:
                self.perform_screening(new_state)
            if new_state == HealthStates.CIN_2plus:
                break
            k += 1

    def perform_screening(self, current_state):
        if current_state == HealthStates.WELL:
            # Choose screening test based on strategy (Pap, HPV, or Co-test)
            # Perform the test
            # Update patient's state and cost accordingly
            pass
        else:
            # Perform colposcopy
            # Update patient's state and cost accordingly
            pass

class PatientStateMonitor:
    def __init__(self, parameters):
        self.currentState = parameters.initialHealthState
        self.costMonitor = PatientCostMonitor(parameters=parameters)

    def update(self, time_step, new_state):
        self.costMonitor.update(k=time_step, current_state=self.currentState, next_state=new_state)
        self.currentState = new_state

    def get_if_alive(self):
        return self.currentState != HealthStates.DEATH

class PatientCostMonitor:
    def __init__(self, parameters):
        self.params = parameters
        self.totalDiscountedCost = 0

    def update(self, k, current_state, next_state):
        cost = 0.5 * (self.params.annualStateCosts[current_state.value] + self.params.annualStateCosts[next_state.value])
        if next_state == HealthStates.DEATH:
            cost += 0.5 * self.params.annualTreatmentCost
        else:
            cost += self.params.annualTreatmentCost

        self.totalDiscountedCost += econ.pv_single_payment(payment=cost, discount_rate=self.params.discountRate / 2, discount_period=2 * k + 1)

class Cohort:
    def __init__(self, id, pop_size, parameters):
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, n_time_steps):
        for i in range(self.popSize):
            patient = Patient(id=self.id * self.popSize + i, parameters=self.params)
            patient.simulate(n_time_steps)
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)

class CohortOutcomes:
    def __init__(self):
        self.costs = []
        self.statCost = None

    def extract_outcome(self, simulated_patient):
        self.costs.append(simulated_patient.state_monitor.costMonitor.totalDiscountedCost)

    def calculate_cohort_outcomes(self, initial_pop_size):
        self.statCost = stat.SummaryStat(name='Discounted cost', data=self.costs)