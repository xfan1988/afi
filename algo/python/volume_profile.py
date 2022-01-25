import numpy as np
from matplotlib import pyplot as plt
from numpy import arange


def volume_profile_obj_norm():
    """
    :return:    Basic curve object
    """

    v = [0] * 13
    v[0] = 0.12
    v[1] = 0.09
    v[11] = 0.10
    v[12] = 0.15

    for i in arange(2, 11):
        v[i] = (1 - (0.12 + 0.09 + 0.1 + 0.15)) / 9  # Sums to 1.0
    v = np.array(v)

    o_adj = [0] * 13
    o_adj[0] = 0.02
    o_adj[1] = 0.005
    o_adj = np.array(o_adj) - np.array(o_adj).mean()

    c_adj = [0] * 13
    c_adj[11] = 0.01
    c_adj[12] = 0.03
    c_adj = np.array(c_adj) - np.array(c_adj).mean()

    auct_avgdev = [0.01, 0.01, 0.09, 0.06]

    Dict = {'base_curve': v, 'o_adj': o_adj, 'c_adj': c_adj, 'auct_avgdev': auct_avgdev}

    return Dict


def plot_volume_profile(openRatio=0.02, closeRatio=0.2):
    vpobj = volume_profile_obj_norm()
    z_open = (openRatio - vpobj['auct_avgdev'][0]) / vpobj['auct_avgdev'][1]
    z_close = (closeRatio - vpobj['auct_avgdev'][2]) / vpobj['auct_avgdev'][3]

    fit = vpobj['base_curve'] + vpobj['o_adj'] * z_open + vpobj['c_adj'] * z_close
    base = vpobj['base_curve']

    fit = fit / fit.sum()

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(base.cumsum(), label='Base', alpha=0.5)
    ax.plot(fit.cumsum(), label='Option Expiry', alpha=0.5)

    ax.set_ylim([0, 1])
    ax.set_xticks(arange(1, 13))
    # ax.set_xticklabels(["ABC"]*12)

    plt.xlabel("Time")

    ax.grid(color='lightgrey')
    ax.legend(frameon=False, fontsize=10)

    fig_file = "C:/temp/volume_profile_curve.jpg"
    print("saving %s" % fig_file)
    plt.savefig(fig_file)
    # plt.show()

    return fit


# def intraday_time_grid():
#     """ Add xlabels """
#     pass


if __name__ == '__main__':

    plot_volume_profile()

