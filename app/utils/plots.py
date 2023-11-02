import matplotlib.pyplot as plt
import matplotlib
import traceback
import datetime
from flask import jsonify

def format_cash(amount):
    def truncate_float(number, places):
        return int(number * (10 ** places)) / 10 ** places

    if amount < 1e3:
        return amount

    if 1e3 <= amount < 1e5:
        return str(truncate_float((amount / 1e5) * 100, 2)) + " K"

    if 1e5 <= amount < 1e7:
        return str(truncate_float((amount / 1e7) * 100, 2)) + " L"

    if amount >= 1e7:
        return str(truncate_float(amount / 1e7, 2)) + " Cr"
    

'''
{
  "chart_properties":{
      "plot_type": "line_graph",
      "x_label": "MONTH",
      "y_label": "AMOUNT",
      "legend": ["Logins"],
      "grid_line_show": "Y",
      "hide_axis_line": ['top', 'right']
    },
    "chart_value":{
      "X":["Jan","Feb","Mar", "Apr","May","Jun"],
      "Y":[20000000,10000000,20000000,30000000,35000000,40000000]
    }
  }

'''    

def single_line_or_bar_graph(input_json, output_path):
    try:
        x = input_json['chart_value']['X']
        y = input_json['chart_value']['Y']
        legend_list = input_json['chart_properties'].get('legend')
        grid_line_show = input_json['chart_properties'].get('grid_line_show')
        hide_axix= input_json['chart_properties'].get('hide_axis_line')
        kind= input_json['chart_properties'].get('plot_type', "line_graph")
        x_label = input_json['chart_properties'].get('x_label')
        y_label = input_json['chart_properties'].get('y_label')
    
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE": "E", "RESPONSE_MSG": "Key Missing", "Error": meta})

    #set_theme
    plt.style.use("seaborn-bright")
    fig, ax1 = plt.subplots(constrained_layout=True,figsize = (10,5))
    
    #set range 
    plt.ylim([0, max(y)+(max(y)/4)])

    if kind == "line_graph":
        #plot line graph        
        plt.plot(x, y, color='#D8D8D8', linewidth = 1.25, marker='o', markerfacecolor="#FF4D15", markersize=10)

    elif kind == "bar_graph":
        #plot line graph
        plt.bar(x,y,color='#de5236',align='center',width=0.5)
    
    else:
        return jsonify({"RESPONSE": "E", "RESPONSE_MSG": "kind should be 'line_graph' or 'bar_graph' only", "Error": meta})
    
    #set labels
    plt.ylabel(x_label, weight=600, fontsize=16)
    plt.xlabel(y_label, weight=600, fontsize=16)

    # to control scientific notation in matplotlib
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    #add legend
    if legend_list:
        plt.legend(legend_list, loc='upper left')
    
    #set grid
    ax1.set_axisbelow(True) #grids behind the bars
    if grid_line_show:
        if kind == "line_graph":
            plt.grid(linestyle = '--',linewidth=0.5, color= '#D6D3D3')
        else:
            plt.grid(axis = 'y', linestyle = '--',linewidth=0.5,color= '#D6D3D3')

    #set formatting
    ticks_loc = ax1.get_yticks().tolist()
    ticks_loc_new = [format_cash(i) for i in ticks_loc]
    ax1.set_yticks(ax1.get_yticks().tolist())
   
    ax1.set_yticklabels(ticks_loc_new,weight=600 ,fontsize=16)
    ax1.set_xticklabels(x, weight=600 ,fontsize=16)

    # here i remove the top and right axis lines in matplotlib.
    if hide_axix!=None:
        ax1.spines[hide_axix].set_visible(False)

    #showing max amount on graphs
    try:
        nxt_index= ticks_loc.index(0.0) +1 # this index is used to show values above the points
    except:
        nxt_index = 0

    if kind == "line_graph":
        for index in range(len(y)):
            ax1.text(x[index], y[index]+(ticks_loc[nxt_index]/1.1), format_cash(y[index]),ha="center", 
                     size=12,style ='normal',fontweight =600,color='white', 
                     bbox ={'facecolor':"#FF4C14",'alpha':1, "boxstyle": "round, pad=0.7", 'color':'#FF4C14'})     
        
        # ###############set arrow################ not working properly##########
        # for i in range(len(x)):
        #     ax1.annotate('', xy=(x[i], y[i]+(ticks_loc[nxt_index]/5)), xytext=(x[i], y[i]+(ticks_loc[nxt_index]/1.15)),
        #                     arrowprops=dict(arrowstyle='-|>', color='#FF4D15', lw=5,mutation_scale=23))
            
    else:
        for i in range(len(x)):
            plt.text(i, y[i]+(ticks_loc[nxt_index]/6), format_cash(y[i]), ha = 'center',fontsize=13,fontweight ='bold')


    x_min, x_max = ax1.get_xlim()
     
    # set x and y limits
    if kind == "bar_graph":
        ax1.set_xlim((x_min*1.5), x_max)
    else:
        ax1.set_xlim((x_min*3), x_max)

    # get the current position of the axis
    pos = ax1.get_position()
    # create a new position tuple with a smaller left value
    new_pos = (pos.x0 + 0.02, pos.y0, pos.width, pos.height)
    # set the new position of the axis
    ax1.set_position(new_pos)

    #saving fig
    saving_path = output_path + "/" + kind + "_" + str(datetime.datetime.now()).replace(' ','') + ".png"
    fig.savefig(saving_path, dpi = 500)
    plt.close('all')

    return saving_path