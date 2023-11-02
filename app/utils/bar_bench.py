import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable

def get_width(v):
    width_dict = {1: 0.2, 2: 0.20, 3: 0.20, 4: 0.28, 5: 0.36, 6: 0.42, 7: 0.5}
    try:
        return width_dict[v]
    except:
        return 0.5

def bar_graph_with_benchmarks(x_pos, y, data, x_label, y_label, title,
                              sub_title, labels, hide_axis, output_path):

    print("x=  ", x_pos)
    print('y=====', y)
    print('labels===', labels)
    fig, ax1 = plt.subplots(constrained_layout=True, figsize=(10, 5))
    fig.set_tight_layout(True)

    # set x-lim and width of bar
    width = get_width(len(y))
    if (len(y) == 1) or (len(y) == 2):
        ax1.set_xlim((-0.8, len(y)))

    for i in range(len(x_pos)):
        rects = ax1.bar(x_pos[i:i + 2], data['value'][i:i + 2], color=data['color'][i], width=width)
        ax1.bar_label(rects, padding=7, fontsize=12, weight=500)

    # Add labels and title
    plt.xlabel(x_label, fontsize=14, weight=600)
    plt.ylabel(y_label, fontsize=14, weight=600)
    plt.title(title, loc='center', x=0.5, y=1.15, fontsize=14, weight=600)
    plt.suptitle(sub_title, fontsize=12, weight=400, x=0.46, y=0.840, ha="center")

    # set x-labels
    plt.xticks(x_pos, labels)

    # Remove ticks on x-axis
    plt.tick_params(bottom=False)

    # hide axis
    if hide_axis:
        ax1.spines[hide_axis].set_visible(False)

    # set grids
    ax1.set_axisbelow(True)
    plt.grid(linestyle='--', linewidth=0.5, axis="y", color='#D6D3D3')

    ################ Create a colormap benchmark #####################
    colors = ["green", "#FFBF00", "red"]
    cmap = plt.cm.colors.ListedColormap(colors)

    # Add color bar to the side
    norm = plt.Normalize(0, 2)  # Normalize the data range
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Dummy array for the color bar

    # Divide existing axes and create new axes
    # at bottom side of image
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="1%", pad=0.20)

    cbar = plt.colorbar(sm, ticks=np.arange(3), orientation="vertical", cax=cax)

    # Set the label for the color bar
    cbar.set_label('')
    # Set the tick labels
    cbar.set_ticklabels(["Below 1%", "1% To 3%", "Above 3%"])

    # save the chart
    saved_at = output_path + "/bar_plot_" + str(datetime.datetime.now()).replace(' ', '') + ".jpg"
    # plt.show()
    fig.savefig(saved_at, dpi=500)
    plt.close('all')
    return saved_at
