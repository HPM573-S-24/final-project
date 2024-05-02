import deampy.econ_eval as econ
import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path
import deampy.statistics as stat

import P1 as data


def print_outcomes(sim_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval of patient survival time
    survival_mean_CI_text = sim_outcomes.statSurvivalTime.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    stroke_mean_CI_text = sim_outcomes.statNumberStrokes.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=0, form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of number of strokes and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          stroke_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def plot_survival_curves_and_histograms(sim_outcomes_none, sim_outcomes_anti):
    # get survival curves of both treatments
    survival_curves = [
        sim_outcomes_none.nLivingPatients,
        sim_outcomes_anti.nLivingPatients
    ]

    # plot survival curve
    path.plot_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['No Treatment', 'Anticoagulation'],
        color_codes=['blue', 'green'],
        file_name='figs/survival_curves.png'
    )

    # histograms of survival times
    set_of_survival_times = [
        sim_outcomes_none.survivalTimes,
        sim_outcomes_anti.survivalTimes
    ]

    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['No Treatment', 'Anticoagulation'],
        color_codes=['blue', 'green'],
        transparency=0.5,
        file_name='figs/survival_times.png'
    )

    stroke_numbers = [
        sim_outcomes_none.nStrokes,
        sim_outcomes_anti.nStrokes
    ]

    # histogram of number of strokes
    hist.plot_histograms(
        data_sets=stroke_numbers,
        title='Histogram of Number of Strokes',
        x_label='Number of Strokes',
        y_label='Count',
        bin_width=1,
        legends=['No Treatment', 'Anticoagulation'],
        color_codes=['blue', 'green'],
        transparency=0.5,
        file_name='figs/number_of_strokes.png'
    )


def print_comparative_outcomes(sim_outcomes_none, sim_outcomes_anti):
    increase_survival_time = stat.DifferenceStatIndp(
        name='Increase in mean survival time',
        x=sim_outcomes_anti.survivalTimes,
        y_ref=sim_outcomes_none.survivalTimes)

    # estimate and CI
    estimate_CI = increase_survival_time.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean survival time and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    increase_stroke_number = stat.DifferenceStatIndp(
        name='Decrease in number of strokes',
        x=sim_outcomes_anti.nStrokes,
        y_ref=sim_outcomes_none.nStrokes)

    # estimate and CI
    estimate_CI = increase_stroke_number.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in number of strokes and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    increase_discounted_cost = stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_anti.costs,
        y_ref=sim_outcomes_none.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2, form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    increase_discounted_utility = stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_anti.utilities,
        y_ref=sim_outcomes_none.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)


def report_CEA_CBA(sim_outcomes_none, sim_outcomes_anti):
    # define two strategies
    none_therapy_strategy = econ.Strategy(
        name='No Treatment',
        cost_obs=sim_outcomes_none.costs,
        effect_obs=sim_outcomes_none.utilities,
        color='green'
    )

    anticoagulation_therapy_strategy = econ.Strategy(
        name='Anticoagulation',
        cost_obs=sim_outcomes_anti.costs,
        effect_obs=sim_outcomes_anti.utilities,
        color='blue'
    )

    # do CEA
    # (the first strategy in the list of strategies is assumed to be the 'Base' strategy)
    CEA = econ.CEA(
        strategies=[none_therapy_strategy, anticoagulation_therapy_strategy],
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
        strategies=[none_therapy_strategy, anticoagulation_therapy_strategy],
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
