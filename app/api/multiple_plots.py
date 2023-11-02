import traceback
from flask import Blueprint, request, jsonify
import shutil
import os
import base64
import datetime
from common.common import get_random_dir_file_name
from visuals.multi_bargraphs import create_multi_graph


multiple_bar = Blueprint('multiple_bar', __name__, url_prefix='/visualization_api')


def image_to_base64(f):
    with open(f, 'rb') as image:
        encoded_string = base64.b64encode(image.read())
    return encoded_string


@multiple_bar.route("/multi_bars", methods= ['POST'])
def kotak_performance_report():
    try:
        input_data = request.get_json()
        print("****************** input_data*************\n\n", input_data)
    
    except Exception as e:
        return jsonify(
            {"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Unable to get data", "Error": str(e)})

    
    try:
        json_data, title = input_data['payload'], input_data['super_title']
        num_plots = len(json_data)

        if num_plots > 8:
            return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "unable to Draw more than 8 plots"})

    
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Mandatory Keys Missing", "Error": meta})

    # save file into folder
    name = get_random_dir_file_name(prefix="", suffix="doc")
    path = "./output/kotak_visuals/" + str(name)

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    
    try:
        kotak_insigts_plots = create_multi_graph(json_data, title, path)
        encoded_graph = image_to_base64(kotak_insigts_plots)
        image_base64 = encoded_graph.decode("utf-8")
        
    
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Some Error Occured", "Error": meta})
    
    try:
        shutil.rmtree('./output/kotak_visuals/')
    except:
        pass

    return jsonify({"RESPONSE_TYPE": "I", "RESPONSE_MESSAGE":"Scuuess", "DATA":image_base64})

