import traceback
from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
import os
import base64
import shutil
import datetime
from common.common import get_random_dir_file_name
from visuals.bar_bench import bar_graph_with_benchmarks


single_bar_graph = Blueprint('single_bar_graph', __name__, url_prefix='/visualization_api')

'''
input req format for this:

{"payload":{"Mon":1.6,"Tue":0.9,"Wed":4.7,"Thu":2.5,"Fri":0.2,"Sat":3.3,"Sun":0.3},"properties":{"x_label":"Days","y_label":"Values in %","title":"Ecosystem Availability Insight","subtitle":"Third Party Rest/Soap APIs","hide_axis":["top","right"]}}

'''

def image_to_base64(f):
    with open(f, 'rb') as image:
        encoded_string = base64.b64encode(image.read())
    return encoded_string

@single_bar_graph.route("/single_bar", methods= ['POST'])
def performance_report():
    try:
        try:
            input_req = request.get_json()
        except Exception as e:
            return jsonify(
                {"RESPONSE": "E", "RESPONSE_MSG": "Unable to get data", "Error": str(e)})

        try:
            # Extract x and y values from JSON data
            labels = input_req['payload'].keys()
            x_pos = np.arange(len(labels))
            y = input_req['payload'].values()
            header_title = input_req['properties']['title']
            subheader_title = input_req['properties']['subtitle']
            x_label = input_req['properties']['x_label']
            y_label = input_req['properties']['y_label']
            hide_axis = input_req['properties']['hide_axis']

            # now make a Dataframe
            list_of_tuples = list(zip(labels, y))
            data = pd.DataFrame(list_of_tuples,
                                columns=['day', 'value'])
            # here i add new column
            data['color'] = data['value'].apply(get_line_color)
            data['color'] = data['color'].astype('category')

        except Exception as ex:
            meta = {
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            }
            return jsonify({"RESPONSE": "E", "RESPONSE_MSG": "Key Missing", "Error": meta})

        # save file into folder
        name = get_random_dir_file_name(prefix="", suffix="doc")
        path = "./output/kotak_visuals/" + str(name)

        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        try:
            data = bar_graph_with_benchmarks(x_pos, y, data, x_label, y_label,
                                            header_title, subheader_title,
                                            labels, hide_axis, output_path=path)

            encoded_graph = image_to_base64(data)
            image_base64 = encoded_graph.decode("utf-8")
        except Exception as ex:
            meta = {
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            }
            return jsonify({"RESPONSE": "E", "RESPONSE_MSG": "Some Error occured", "Error": meta})

        try:
            shutil.rmtree(path)
        except:
            pass

        return jsonify({"RESPONSE_TYPE": "I", "RESPONSE_MESSAGE":"Scuuess", "DATA":image_base64})
    
    except Exception as ex:
            meta = {
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            }
            return jsonify({"RESPONSE": "E", "RESPONSE_MSG": "Some Error occured", "Error": meta})



# Define the function to determine the line color
def get_line_color(y):
    if y < 1:
        return 'green'
    elif 1 < y <= 3:
        return '#FFBF00'
    else:
        return 'red'