import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import jsonify
import datetime
import traceback
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches

def get_width(v):
    width_dict = {1: 0.2, 2: 0.20, 3: 0.20, 4: 0.28, 5: 0.36, 6: 0.42, 7: 0.5}
    try:
        return width_dict[v]
    except:
        return 0.5
    

# Define the function to determine the line color
def get_line_color(y):
    if y < 1:
        return 'green'
    elif 1 < y <= 3:
        return '#FFBF00'
    else:
        return 'red'
    
def multi_bar(ax, json_data):
    for i, data in enumerate(json_data):
        x = data["x"]
        y = data["y"]
        try:
            bar_color = data['bar_color']
        except:
            pass

        try:
            leg = data['remarks']
            final_legends = []
            for c, l in leg.items():
                final_legends.append(mpatches.Patch(color=c, label=l))
            legends = final_legends
        except:
            legends = ''

        ## set theme
        ax[i].patch.set_facecolor('#F8F8FF')
        ax[i].patch.set_alpha(0)
        
        ####################
        list_of_tuples = list(zip(x, y))
        df = pd.DataFrame(list_of_tuples,
                            columns=['X', 'value'])
        
        
        #handling missing values
        df['value'].replace(['', ' ', 'null', 'Null', 'na', 'NA', np.nan, 'NaN'],
                                         0, inplace=True)
        df["value"] = df["value"].astype(float)
        
        # here i add new column
        df['color'] = bar_color
        df['color'] = df['color'].astype('category')
        
        #####################
        
        ax[i].bar(df['X'], df['value'], width= get_width(len(df['value'])), color=df['color'],align='center')
        
        #set title and label
        ax[i].set_xlabel(data["x_label"],fontsize=14, weight=600)
        ax[i].set_ylabel(data["y_label"],fontsize=14, weight=600)
        ax[i].set_title(data["title"],fontsize=18, weight=400)
        # add the legend
        ax[i].legend(handles=legends, loc='best', borderaxespad=0, fontsize=10, frameon=False)
        # Remove ticks on x-axis
        ax[i].tick_params(bottom=False)
        # grids
        ax[i].set_axisbelow(True)
        ax[i].grid(linestyle = '--',linewidth=0.5, color= '#D6D3D3', axis='y')
        
        #show labels on bar but problem when 2 json_objects comes
        for pos in range(len(y)):
            ax[i].text(pos, df['value'][pos], df['value'][pos], ha = 'center', fontsize=14 )

def single_bar(ax, json_data):
    for data in json_data:
        x = data["x"]
        y = data["y"]

        try:
            bar_color = data['bar_color']
        except:
            pass

        try:
            leg = data['remarks']
            final_legends = []
            for c, l in leg.items():
                final_legends.append(mpatches.Patch(color=c, label=l))
            legends = final_legends
        except:
            legends = ''
        
        # set theme 
        ax.patch.set_facecolor('#F8F8FF')
        ax.patch.set_alpha(0)

       
        if len(y)<=2:
            ax.set_xlim(-0.75, len(y))
            width = 0.2
        else:
            width = 0.3


        ####################
        list_of_tuples = list(zip(x, y))
        df = pd.DataFrame(list_of_tuples,
                            columns=['X', 'value'])


        #handling missing values
        df['value'].replace(['', ' ', 'null', 'Null', 'na', 'NA', np.nan, 'NaN'],
                                         0, inplace=True)
        df["value"] = df["value"].astype(float)

        # here i add new column
        df['color'] = bar_color
        df['color'] = df['color'].astype('category')

        #####################
        
        ax.bar(df['X'], df['value'], width=width, color=df['color'],align='center')
        
        # set title and labels
        ax.set_xlabel(data["x_label"],fontsize=14, weight=600)
        ax.set_ylabel(data["y_label"],fontsize=14, weight=600)
        ax.set_title(data["title"],fontsize=18, weight=400)
        # add the legend
        ax.legend(handles= legends, loc='best', borderaxespad=0, fontsize=10, frameon=False)
        # Remove ticks on x-axis
        ax.tick_params(bottom=False)
        # grids
        ax.set_axisbelow(True)
        ax.grid(linestyle = '--',linewidth=0.5, color= '#D6D3D3', axis='y')
        # hide side axis
        ax.spines[['top', "right"]].set_visible(False)
        #show labels on bar but problem when 2 json_objects comes
        for pos in range(len(y)):
            ax.text(pos, df['value'][pos], df['value'][pos], ha = 'center', fontsize=14)



def create_multi_graph(json_data, super_title, output_path):
    num_plots = len(json_data)

    if num_plots > 2:
        nrows = num_plots // 2 + num_plots % 2
        ncols = 2
        fig_size = (20,15)
    elif num_plots == 2:
        nrows =2
        ncols =1
        fig_size = (10,10)
    else:
        nrows =1
        ncols =1
        fig_size = (10,6)

    try:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=fig_size, constrained_layout=True)
        
        #set background
        fig.patch.set_facecolor('#EBF4FA')
        fig.patch.set_alpha(1)
        
        if num_plots >= 2:
            ax = axes.flatten()
            multi_bar(ax, json_data)
        else:
            single_bar(axes, json_data)
            
        #If the number of plots is odd, remove the last empty subplot
        
        if ((num_plots>2) and (num_plots % 2 != 0)):
            fig.delaxes(axes[-1, -1])
            
        
        # Title the figure
        fig.suptitle(super_title, fontsize=20, fontweight='bold')
        fig_path = output_path + "/bar_plot_" + str(datetime.datetime.now()).replace(' ', '') + ".jpg"
        
        fig.savefig(fig_path, dpi=200)
        plt.close('all')

        print(f'\nGraph successfully saved at path: {fig_path}')
        return fig_path

    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Graph is not saved", "Error": meta})


