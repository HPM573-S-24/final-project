import input_data as data
import model_classes as model
import param_classes as param
import support as support

# simulating pap test
# create a cohort
cohort_pap = model.Cohort(id=0,
                          pop_size=data.POP_SIZE,
                          parameters=param.Parameters(therapy=param.Therapies.PAP_TEST))
# simulate the cohort
cohort_pap.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating HPV test
# create a cohort
cohort_HPV = model.Cohort(id=1,
                          pop_size=data.POP_SIZE,
                          parameters=param.Parameters(therapy=param.Therapies.HPV_TEST))
# simulate the cohort
cohort_HPV.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating co test
# create a cohort
cohort_co = model.Cohort(id=2,
                         pop_size=data.POP_SIZE,
                         parameters=param.Parameters(therapy=param.Therapies.CO_TEST))
# simulate the cohort
cohort_co.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time
support.print_outcomes(sim_outcomes=cohort_pap.cohortOutcomes,
                       therapy_name=param.Therapies.PAP_TEST)
support.print_outcomes(sim_outcomes=cohort_HPV.cohortOutcomes,
                       therapy_name=param.Therapies.HPV_TEST)
support.print_outcomes(sim_outcomes=cohort_co.cohortOutcomes,
                       therapy_name=param.Therapies.CO_TEST)

# plot survival curves and histograms
support.plot_histograms(sim_outcomes_pap=cohort_pap.cohortOutcomes,
                        sim_outcomes_HIV=cohort_HPV.cohortOutcomes,
                        sim_outcomes_co=cohort_co.cohortOutcomes)

# print comparative outcomes
support.print_comparative_outcomes(sim_outcomes_pap=cohort_pap.cohortOutcomes,
                                   sim_outcomes_co=cohort_co.cohortOutcomes)

# report the CEA results
support.report_CEA_CBA(sim_outcomes_pap=cohort_pap.cohortOutcomes,
                       sim_outcomes_co=cohort_co.cohortOutcomes)
