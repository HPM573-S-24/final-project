import input_data as data
import model_classes as model
import param_classes as param
import support as support

# simulating pap test
# create a cohort
cohort_pap = model.Cohort(id=0,
                          pop_size=data.POP_SIZE,
                          parameters=param.Parameters(test=param.Tests.PAP_TEST))
# simulate the cohort
cohort_pap.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating HPV test
# create a cohort
cohort_HPV = model.Cohort(id=1,
                          pop_size=data.POP_SIZE,
                          parameters=param.Parameters(test=param.Tests.HPV_TEST))
# simulate the cohort
cohort_HPV.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating co test
# create a cohort
cohort_co = model.Cohort(id=2,
                         pop_size=data.POP_SIZE,
                         parameters=param.Parameters(test=param.Tests.CO_TEST))
# simulate the cohort
cohort_co.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time
support.print_outcomes(sim_outcomes=cohort_pap.cohortOutcomes,
                       test_name=param.Tests.PAP_TEST)
support.print_outcomes(sim_outcomes=cohort_HPV.cohortOutcomes,
                       test_name=param.Tests.HPV_TEST)
support.print_outcomes(sim_outcomes=cohort_co.cohortOutcomes,
                       test_name=param.Tests.CO_TEST)

# plot histograms
support.plot_histograms(sim_outcomes_pap=cohort_pap.cohortOutcomes,
                        sim_outcomes_HPV=cohort_HPV.cohortOutcomes,
                        sim_outcomes_co=cohort_co.cohortOutcomes)

# print comparative outcomes
support.print_comparative_outcomes(sim_outcomes_pap=cohort_pap.cohortOutcomes,
                                   sim_outcomes_HPV=cohort_HPV.cohortOutcomes,
                                   sim_outcomes_co=cohort_co.cohortOutcomes)

# report the CEA results
support.report_CEA_CBA(sim_outcomes_pap=cohort_pap.cohortOutcomes,
                       sim_outcomes_HPV=cohort_HPV.cohortOutcomes,
                       sim_outcomes_co=cohort_co.cohortOutcomes)
