import deampy.econ_eval as econ
import deampy.plots.histogram as hist
import deampy.statistics as stat

import input_data as data


def print_outcomes(sim_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """

    potential_cancer_mean_CI_text = sim_outcomes.statNumCancer.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=0, form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of number of potential cervical cancer cases detected and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          potential_cancer_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def plot_histograms(sim_outcomes_pap, sim_outcomes_HIV, sim_outcomes_co):
    potential_cancer_numbers = [
        sim_outcomes_pap.nPotentialCancer,
        sim_outcomes_HIV.nPotentialCancer,
        sim_outcomes_co.nPotentialCancer
    ]

    # histogram of number of potential cancer cases detected
    hist.plot_histograms(
        data_sets=potential_cancer_numbers,
        title='Histogram of Number of potential cancer cases detected',
        x_label='Number of potential cancer cases detected',
        y_label='Count',
        bin_width=1,
        legends=['Pap Test', 'HIV test', 'Co Test'],
        color_codes=['blue', 'green', 'red'],
        transparency=0.5,
        file_name='figs/number_of_potential_cancer.png'
    )


def print_comparative_outcomes(sim_outcomes_pap, sim_outcomes_co):
    increase_potential_cancer_number = stat.DifferenceStatIndp(
        name='Change in number of potential cancer cases detected',
        x=sim_outcomes_pap.nPotentialCancer,
        y_ref=sim_outcomes_co.nPotentialCancer)

    # estimate and CI
    estimate_CI = increase_potential_cancer_number.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in number of potential cancer cases detected and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    increase_discounted_cost = stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_pap.costs,
        y_ref=sim_outcomes_co.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2, form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    increase_discounted_utility = stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_pap.utilities,
        y_ref=sim_outcomes_co.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)


def report_CEA_CBA(sim_outcomes_pap, sim_outcomes_co):
    # define two strategies
    pap_test_strategy = econ.Strategy(
        name='Pap test',
        cost_obs=sim_outcomes_pap.costs,
        effect_obs=sim_outcomes_pap.utilities,
        color='green'
    )

    co_test_strategy = econ.Strategy(
        name='Co test',
        cost_obs=sim_outcomes_co.costs,
        effect_obs=sim_outcomes_co.utilities,
        color='blue'
    )

    # do CEA
    # (the first strategy in the list of strategies is assumed to be the 'Base' strategy)
    CEA = econ.CEA(
        strategies=[pap_test_strategy, co_test_strategy],
        if_paired=False
    )

    # plot cost-effectiveness figure
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional QALYs',
        y_label='Additional Cost',
        interval_type='c',  # to show confidence intervals for cost and effect of each strategy
        file_name='figs/cea.png'
    )

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    CBA = econ.CBA(
        strategies=[pap_test_strategy, co_test_strategy],
        wtp_range=[0, 100000],
        if_paired=False
    )
    # show the net monetary benefit figure
    CBA.plot_marginal_nmb_lines(
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay per QALY ($)',
        y_label='Marginal Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5),
        file_name='figs/nmb.png'
    )
