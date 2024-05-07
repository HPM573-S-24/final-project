import deampy.econ_eval as econ
import input_data as data


def print_outcomes(sim_outcomes, test_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param test_name: the name of the selected test
    """

    potential_cancer_mean_CI_text = sim_outcomes.statNumCancer

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=0, form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(test_name)
    print("  Estimate of number of potential cervical cancer cases detected:".format(1 - data.ALPHA, prec=0),
          potential_cancer_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def report_CEA_CBA(sim_outcomes_pap, sim_outcomes_co, sim_outcomes_HPV):
    # Define strategies for each test
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

    hpv_test_strategy = econ.Strategy(
        name='HPV test',
        cost_obs=sim_outcomes_HPV.costs,
        effect_obs=sim_outcomes_HPV.utilities,
        color='red'
    )

    # Perform cost-effectiveness analysis (CEA)
    CEA = econ.CEA(
        strategies=[co_test_strategy, pap_test_strategy, hpv_test_strategy],
        if_paired=False
    )

    # Plot cost-effectiveness plane
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional Potential Cervical Cancer Case Detected',
        y_label='Additional Cost',
        interval_type='c',  # Show confidence intervals for cost and effect of each strategy
        file_name='figs/cea.png'
    )

    # Build the cost-effectiveness table
    CEA.build_CE_table(
        interval_type='c',
        alpha=data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv'
    )

    # Perform cost-benefit analysis (CBA)
    CBA = econ.CBA(
        strategies=[co_test_strategy, pap_test_strategy, hpv_test_strategy],
        wtp_range=[0, 100000],  # Range of willingness-to-pay per Potential Cervical Cancer Case Detected
        if_paired=False
    )

    # Plot net monetary benefit figure
    CBA.plot_marginal_nmb_lines(
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay per Potential Cervical Cancer Case Detected',
        y_label='Marginal Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5),
        file_name='figs/nmb.png'
    )

