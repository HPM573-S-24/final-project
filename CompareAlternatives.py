import input_data as data
import model_classes as model
import param_classes as param
import support as support

# simulating no treatment
# create a cohort
cohort_none = model.Cohort(id=0,
                           pop_size=data.POP_SIZE,
                           parameters=param.Parameters(therapy=param.Therapies.NONE))
# simulate the cohort
cohort_none.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating anticoagulation
# create a cohort
cohort_anti = model.Cohort(id=1,
                           pop_size=data.POP_SIZE,
                           parameters=param.Parameters(therapy=param.Therapies.ANTI))
# simulate the cohort
cohort_anti.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time
support.print_outcomes(sim_outcomes=cohort_none.cohortOutcomes,
                       therapy_name=param.Therapies.NONE)
support.print_outcomes(sim_outcomes=cohort_anti.cohortOutcomes,
                       therapy_name=param.Therapies.ANTI)

# plot survival curves and histograms
support.plot_survival_curves_and_histograms(sim_outcomes_none=cohort_none.cohortOutcomes,
                                            sim_outcomes_anti=cohort_anti.cohortOutcomes)

# print comparative outcomes
support.print_comparative_outcomes(sim_outcomes_none=cohort_none.cohortOutcomes,
                                   sim_outcomes_anti=cohort_anti.cohortOutcomes)

# report the CEA results
support.report_CEA_CBA(sim_outcomes_none=cohort_none.cohortOutcomes,
                       sim_outcomes_anti=cohort_anti.cohortOutcomes)
