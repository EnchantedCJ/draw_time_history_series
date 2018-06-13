# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import os


def draw_dual(i, top, bottom):
    fig = plt.figure(figsize=(4.56, 1.44))
    # ax = fig.add_subplot(111)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.patch.set_facecolor('k')
    ax.plot(top[:, 0], top[:, 1], color='r', linewidth=0.5, zorder=10)
    ax.plot(bottom[:, 0], bottom[:, 1], color='c', linewidth=0.5, zorder=10)
    ax.scatter(top[i, 0], top[i, 1], color='r', linewidth=1, zorder=20)
    ax.scatter(bottom[i, 0], bottom[i, 1], color='c', linewidth=1, zorder=20)
    ylim = ax.get_ylim()
    ylim = max(map(abs, ylim))
    ax.set_ylim(-1.1 * ylim, 1.1 * ylim)
    xlim = ax.get_xlim()
    ax.set_xlim(-3, xlim[1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_position(('data', 0))
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['left'].set_color('w')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['bottom'].set_color('w')
    plt.savefig('./series/time_history' + str(i), dpi=600, facecolor='none')
    plt.clf()
    plt.close()


def draw_single(i, eq):
    fig = plt.figure(figsize=(4.56, 1.44))
    # ax = fig.add_subplot(111)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.patch.set_facecolor('k')
    ax.plot(eq[:, 0], eq[:, 1], color='c', linewidth=0.5, zorder=10)
    ax.scatter(eq[i, 0], eq[i, 1], color='r', linewidth=1, zorder=20)
    ylim = ax.get_ylim()
    ylim = max(map(abs, ylim))
    ax.set_ylim(-1.1 * ylim, 1.1 * ylim)
    xlim = ax.get_xlim()
    ax.set_xlim(-3, xlim[1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_position(('data', 0))
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['left'].set_color('w')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['bottom'].set_color('w')
    plt.savefig('./series/time_history' + str(i), dpi=600, facecolor='none')
    plt.clf()
    plt.close()


def read_config():
    with open('config.txt', 'r', encoding='utf-8') as fConfig:
        temp = fConfig.readline()
        threads = int(fConfig.readline().strip())
        temp = fConfig.readline()
        gms = int(fConfig.readline().strip())
        if gms != 1 and gms != 2:
            return (threads, gms, False)
        else:
            return (threads, gms, True)


def main():
    config = read_config()
    if not config[2]:
        print('Number of GMs should be 1 or 2!')
        return
    threads = config[0]
    gms = config[1]

    if not os.path.exists('./series'):
        os.makedirs('./series')

    print('Parent process %s. ' % os.getpid())
    p = Pool(threads)  # 多进程数

    if gms == 1:
        # draw_single
        eq = np.loadtxt('./EW.txt', skiprows=1)
        cj = eq[:, 0].size
        cj = 1  # for testing
        for i in range(cj):
            p.apply_async(draw_single, args=(i, eq))

    elif gms == 2:
        # draw_dual
        top = np.loadtxt('./top.txt', skiprows=0)
        bottom = np.loadtxt('./bottom.txt', skiprows=0)
        cj = max(top[:, 0].size, bottom[:, 0].size)
        cj = 1  # For testing
        for i in range(cj):
            p.apply_async(draw_dual, args=(i, top, bottom))

    p.close()
    p.join()
    print('Done!')


if __name__ == '__main__':
    main()
