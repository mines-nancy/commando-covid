# -*- coding: utf-8 -*-
""" Invoke as python -m labs.beyond_sir.new_model [options] from the server directory to run the simulator
"""

import warnings

# warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import lmfit

import json

import os.path
from os import mkdir
import datetime
import argparse

from models.rule import RuleChangeField
from labs.defaults import get_default_params, import_json, export_json
from .ModelDiff import model_diff
from .ModelDiscr import model_disc


def initial_code(data, model, series, model_parameters, model_rules):
    def plotter(t, S, E, I, M, C, R, D, R_0, S_1=None, S_2=None, x_ticks=None):
        if S_1 is not None and S_2 is not None:
            print(f"percentage going to ICU: {S_1 * 100}; percentage dying in ICU: {S_2 * 100}")

        f, ax = plt.subplots(1, 1, figsize=(20, 4))
        if x_ticks is None:
            ax.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptibles')
            ax.plot(t, E, 'y', alpha=0.7, linewidth=2, label='Incubés')
            ax.plot(t, I, 'r', alpha=0.7, linewidth=2, label='Infectés')
            ax.plot(t, C, 'r--', alpha=0.7, linewidth=2, label='Soins Intensifs')
            ax.plot(t, R, 'g', alpha=0.7, linewidth=2, label='Rétablis')
            ax.plot(t, D, 'k', alpha=0.7, linewidth=2, label='Décédés')
        else:
            ax.plot(x_ticks, S, 'b', alpha=0.7, linewidth=2, label='Susceptibles')
            ax.plot(x_ticks, E, 'y', alpha=0.7, linewidth=2, label='Incubés')
            ax.plot(x_ticks, I, 'r', alpha=0.7, linewidth=2, label='Infectés')
            ax.plot(x_ticks, C, 'r--', alpha=0.7, linewidth=2, label='Soins Intensifs')
            ax.plot(x_ticks, R, 'g', alpha=0.7, linewidth=2, label='Rétablis')
            ax.plot(x_ticks, D, 'k', alpha=0.7, linewidth=2, label='Décédés')

            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            f.autofmt_xdate()

        ax.title.set_text('extended SEIR-lambda_model_func')

        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        plt.show()

        '''
        f = plt.figure(figsize=(20,4))
        # sp1
        ax1 = f.add_subplot(141)
        if x_ticks is None:
            ax1.plot(t, R_0, 'b--', alpha=0.7, linewidth=2, label='R_0')
        else:
            ax1.plot(x_ticks, R_0, 'b--', alpha=0.7, linewidth=2, label='R_0')
            ax1.xaxis.set_major_locator(mdates.YearLocator())
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax1.xaxis.set_minor_locator(mdates.MonthLocator())
            f.autofmt_xdate()


        ax1.title.set_text('R_0 over time')
        ax1.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax1.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        # sp2
        sigma = 1.0/get_default_params()['parameters']['dm_incub']

        ax2 = f.add_subplot(142)
        total_CFR = [0] + [100 * D[i] / (sum(sigma*E[:i])) if sum(sigma*E[:i])>0 else 0 for i in range(1, len(t))]
        daily_CFR = [0] + [100 * ((D[i]-D[i-1]) / ((R[i]-R[i-1]) + (D[i]-D[i-1]))) if max((R[i]-R[i-1]), (D[i]-D[i-1]))>10 else 0 for i in range(1, len(t))]
        if x_ticks is None:
            ax2.plot(t, total_CFR, 'r--', alpha=0.7, linewidth=2, label='total')
            ax2.plot(t, daily_CFR, 'b--', alpha=0.7, linewidth=2, label='daily')
        else:
            ax2.plot(x_ticks, total_CFR, 'r--', alpha=0.7, linewidth=2, label='total')
            ax2.plot(x_ticks, daily_CFR, 'b--', alpha=0.7, linewidth=2, label='daily')
            ax2.xaxis.set_major_locator(mdates.YearLocator())
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax2.xaxis.set_minor_locator(mdates.MonthLocator())
            f.autofmt_xdate()

        ax2.title.set_text('Fatality Rate (%)')
        ax2.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax2.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        # sp3
        ax3 = f.add_subplot(143)
        newDs = [0] + [D[i]-D[i-1] for i in range(1, len(t))]
        if x_ticks is None:
            ax3.plot(t, newDs, 'r--', alpha=0.7, linewidth=2, label='total')
        else:
            ax3.plot(x_ticks, newDs, 'r--', alpha=0.7, linewidth=2, label='total')
            ax3.xaxis.set_major_locator(mdates.YearLocator())
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax3.xaxis.set_minor_locator(mdates.MonthLocator())
            f.autofmt_xdate()

        ax3.title.set_text('Deaths per day')
        ax3.yaxis.set_tick_params(length=0)
        ax3.xaxis.set_tick_params(length=0)
        ax3.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax3.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        # sp4
        ax4 = f.add_subplot(144)

        if x_ticks is None:

            ax4.plot(t, M, 'b', alpha=0.7, linewidth=2, label='Medical')
            ax4.plot(t, C, 'r--', alpha=0.7, linewidth=2, label='Critical')

            # ax42 = ax4.twinx()  # instantiate a second axes that shares the same x-axis
            # ax42.plot(t, R_0, 'g--', alpha=0.7, linewidth=2, label='R_0')

        else:
            ax4.plot(x_ticks, M, 'b', alpha=0.7, linewidth=2, label='Medical')
            ax4.plot(x_ticks, C, 'r--', alpha=0.7, linewidth=2, label='Critical')
            # ax42.plot(x_ticks, R_0, 'g--', alpha=0.7, linewidth=2, label='R_0')
            ax4.xaxis.set_major_locator(mdates.YearLocator())
            ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax4.xaxis.set_minor_locator(mdates.MonthLocator())
            f.autofmt_xdate()


        ax4.title.set_text('Hospital over time')
        ax4.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax4.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        # f.tight_layout()  # otherwise the right y-label is slightly clipped

        plt.show()
        '''

    if model == 'diff':
        lambda_model_func = lambda p, **kwargs: model_diff(p, **kwargs)
    elif model == 'disc' or model == 'disc_int':
        lambda_model_func = lambda p, **kwargs: model_disc({'parameters': p, 'rules': model_rules}, **kwargs)
    else:
        lambda_model_func = None

    if not args.noplot:
        plotter(*lambda_model_func(model_parameters))

    # parameters
    # data = sortie SM (=SM+SI+SS) de notre modele

    ''' the labels of the following dictionary will appear with the same name in **kwargs
        passed to lambda_model_func() '''
    '''
    params_init_min_max = {"R0_start": (3.0, 2.0, 5.0),
                           "R0_confinement": (0.6, 0.3, 2.0),
                           "R0_end": (0.9, 0.3, 3.5)
                           }  # form: {parameter: (initial guess, minimum value, max value)}
    '''
    ''' @TODO allow passing these parameters and values as a .json input field and add computation of
        proportional default min/max values if non provided '''
    params_init_min_max = {"beta": (3.31 / 9, 2.0 / 9, 5.0 / 9),
                           "beta_post": (0.4 / 9, 0.1 / 9, 2.0 / 9),
                           "patient0": (40, 1, 100),
                           "dm_h": (6, 3, 8)
                           }  # form: {parameter: (initial guess, minimum value, max value)}

    if args.variables:
        with open(args.variables[0]) as json_file:
            opt_variables = json.load(json_file)
            json_file.close()
        params_init_min_max = opt_variables

    #days = len(data)
    # model_parameters['lim_time'] = days
    # y_data = np.array(data)
    # x_data = np.linspace(0, days - 1, days, dtype=int)  # x_data is just [0, 1, ..., max_days] array
    ''' @TODO we are currently assuming x_data goes by integer increments/values. This need not be true '''
    x_data = np.array(data[:, 0], dtype=int)
    y_data = data[:, 1]

    def optimize(x_data, y_data, fitter_function):
        mod = lmfit.Model(fitter_function)
        for kwarg, (init, mini, maxi) in params_init_min_max.items():
            mod.set_param_hint(str(kwarg), value=init, min=mini, max=maxi, vary=True)

        params = mod.make_params()
        result = mod.fit(y_data, params, method=optim, x=x_data)
        # result = mod.fit(y_data, params, method='trust-constr', x=x_data)

        return result

    # x_convert = lambda x : np.where(x_data == x)

    def fitter(x, **kwargs):
        ret = lambda_model_func(model_parameters, **kwargs)
        # return ret[series][x_convert(x)]
        return ret[series][x]

    result = optimize(x_data, y_data, fitter)

    opt_parameters = dict(model_parameters)
    opt_parameters.update(result.best_values)

    if save_output:
        f = open(basename + '.res', 'w')
        f.write(result.fit_report())
        f.write('\n\n')
        f.write(f'Optimal values : {result.best_values}')
        f.close()

        with open(basename + '_opt.json', 'w') as json_file:
            json.dump(result.best_values, json_file)
            json_file.close()

        ''' @TODO find a way to better integrate pre-existing rules and possible other
            confinement dates than the default ones '''
        opt_rules = [r for r in model_rules]
        try:
            t_confinement = get_default_params()['other']['confinement']
            opt_rules += [RuleChangeField(t_confinement, 'beta', opt_parameters['beta_post'])]
        except KeyError:
            pass

        try:
            t_deconfinement = get_default_params()['other']['deconfinement']
            opt_rules += [RuleChangeField(t_deconfinement, 'beta', opt_parameters['beta_end'])]
        except KeyError:
            pass

        export_json(basename + '.json', opt_parameters, opt_rules)
    else:
        print(result.fit_report())
        print('========')
        print(result.best_values)

    if not args.noplot:
        result.plot_fit(datafmt="-")

        full_days = model_parameters['lim_time']
        # first_date = np.datetime64(covid_data.Date.min()) - np.timedelta64(outbreak_shift,'D')
        first_date = np.datetime64('2020-01-06')
        x_ticks = pd.date_range(start=first_date, periods=full_days, freq="D")

        plotter(*lambda_model_func(model_parameters, **result.best_values), x_ticks=x_ticks)

    return lambda_model_func(model_parameters, **result.best_values)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="python -m new_model",
                                     description='Fit MODSIR-19 simulator parameters on provided measured data.')
    parser.add_argument('-p', '--params', metavar='parameters', type=str, nargs=1,
                        help='pathname to initial parameter set (JSON)')
    parser.add_argument('-v', '--variables', metavar='variables', type=str, nargs=1,
                        help='pathname to variable parameter set with bounds (JSON) on which to optimise the fitting '
                             'data')
    parser.add_argument('-i', '--input', metavar='input', type=str, nargs=1,
                        help='input file containing measured parameters (CSV format)')
    parser.add_argument('-d', '--data', metavar='data',
                        choices=['SE', 'INCUB', 'IR', 'IH', 'SM', 'SI', 'SS', 'R', 'DC'], nargs=1, default=['SI'],
                        help="identification of measured data used for optimization ('data' value in 'SE', 'INCUB', "
                             "'IR', 'IH', 'SM', 'SI', 'SS', 'R', 'DC')")
    parser.add_argument('-m', '--model', metavar='model', choices=['diff', 'disc_int', 'disc'], nargs=1,
                        default=['disc'],
                        help="Simulator model to use : differential, discrete state with integer flux, discrete state "
                             "with continuous flux ('model' value in 'diff', 'disc', 'disc_int')")
    parser.add_argument('--opt', metavar='optimiser', choices=['least-squares', 'trust-constr'], nargs=1,
                        default=['least-squares'],
                        help="Simulator model to use : differential, discrete state with integer flux, discrete state "
                             "with continuous flux ('model' value in 'diff', 'disc', 'disc_int')")
    parser.add_argument('--noplot', action='store_true', help="do not display obtained curves")
    parser.add_argument('-s', '--save', metavar='prefix', type=str, nargs='?',
                        help='filename prefix to output obtained curve points in .csv file format')
    parser.add_argument('-n', metavar='points', type=int, nargs=1,
                        help="number of data points to consider for training")
    parser.add_argument('--path', metavar='pathname', type=str, nargs=1,
                        help='to be used with -s, --save parameter. Saves output files to provided path')

    ''' @TODO take into account --path arguments.
        Current behaviour is to take default parameters and to optimise for 'SI'
    '''

    args = parser.parse_args()

    default_model_params = get_default_params()
    day0 = default_model_params['data']['day0']

    read_target = None
    if args.input:
        read_target = pd.read_csv(args.input[0], sep=';').to_numpy()
        target = read_target
    else:
        default_data = default_model_params['data']['data_chu_rea']
        target = np.array([[x - day0, y] for (x, y) in default_data.items() if y]).reshape([-1, 2])

    if args.n:
        target = target[:args.n[0], ]

    if args.params:
        model_parameters, model_rules, other = import_json(args.params[0])
    else:
        model_parameters = default_model_params['parameters']
        model_rules = default_model_params['rules']

    if args.model[0] == 'disc_int':
        model_parameters['integer_flux'] = True

    optim = args.opt[0]

    ''' @TODO the following hack is ugly and requires models to return data at the
        sames positions as those indexed below ... it would be better if models returned
        their data as a dictionary '''
    series = {'SE': 1, 'INCUB': 2, 'I': 3, 'SM': 4, 'SI': 5, 'R': 6, 'DC': 7}

    if args.path:
        outputdir = args.path[0] + '/'
    else:
        outputdir = "./outputs/"

    if 'save' in vars(args).keys():
        save_output = True
    else:
        save_output = False

    if save_output:
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        timestamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S_")

        if args.save:
            basename = outputdir + timestamp + args.save
        else:
            basename = outputdir + timestamp + 'commando_covid_fit_' + args.model[0] + '_' + optim

    initial_code(target, args.model[0], series[args.data[0]], model_parameters, model_rules)
