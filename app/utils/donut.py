import traceback
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from flask import jsonify

def donut_graph(json_data, output_path):
    try:
        data = json_data['chart_value']['data']
        label_list = json_data["chart_value"]['label']
        explode_list = json_data['chart_properties']['explode']
        legend_list = json_data['chart_value']['legend']
        title = json_data['chart_properties']['title']
        center_value = json_data['chart_properties']["center_value"]
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return {"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Mandatory Keys Missing", "Error": meta}


    if explode_list:
        explode = tuple(explode_list)
    else:
        explode = None

    if json_data['chart_properties']["show_labels"]=="Y":
        labels = label_list
    else:
        labels = None
    
    if json_data["chart_properties"]["show_legends"]=="Y":
        legends = legend_list
    else :
        legends = []

    colors = sns.color_palette('pastel')
    fig, ax = plt.subplots(constrained_layout=False)

    if json_data["chart_properties"]["show_percentage"] == "Y":
        # total = sum(data)
        # data = data/total*100
        plt.pie(data, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.75,explode=explode)
        circle = plt.Circle( (0,0), 0.5, color='white')
        p=plt.gcf()
        p.gca().add_artist(circle)
        

    else:
        # Create a pieplot
        plt.pie(data, labels= labels, colors=colors, explode=explode_list)

        # add a circle at the center to transform it in a donut chart
        my_circle=plt.Circle( (0,0), 0.5, color='white')
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        
    plt.legend(legends, bbox_to_anchor=(1,0.5), loc="center right", fontsize=10, 
        bbox_transform=plt.gcf().transFigure)
        
    ax.text(0., 0., center_value, horizontalalignment='center', verticalalignment='center',size=15,fontweight ='bold')
    
    # adjust    
    plt.subplots_adjust(left=None, bottom=None, right=0.5, top=None, wspace=None, hspace=None)
    #title
    plt.title(title,loc='center',x=0.5, y=1.15, fontsize=18, fontweight="bold")

    saving_path = output_path +"/donut_" + str(datetime.datetime.now()).replace(' ','') + ".png"
    
    plt.savefig(saving_path, dpi=300)
    plt.close('all')
    
    return saving_path
