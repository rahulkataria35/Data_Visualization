import traceback
from flask import Blueprint, request, jsonify
import shutil
import os
import base64
from common.common import get_random_dir_file_name
from utils.donut import donut_graph


donut_chart = Blueprint('donut_chart', __name__, url_prefix='/visualization_api')


def image_to_base64(f):
    with open(f, 'rb') as image:
        encoded_string = base64.b64encode(image.read())
    return encoded_string


@donut_chart.route("/donut", methods= ['POST'])
def donut():
    try:
        input_data = request.get_json()
        print("****************** input_data*************\n\n", input_data)
    
    except Exception as e:
        return jsonify(
            {"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Unable to get data", "Error": str(e)})

    
    try:
        json_data = input_data['payload']
    
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Mandatory Keys Missing", "Error": meta})

    # save file into folder
    name = get_random_dir_file_name(prefix="", suffix="doc")
    path = "./output/donut/" + str(name)

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    
    try:
        donut_response = donut_graph(json_data, path)
        try:
            if donut_response["RESPONSE_TYPE"] == "E":
                return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Mandatory Keys Missing", "Error": donut_response['Error']})
        except:
            encoded_graph = image_to_base64(donut_response)
            image_base64 = encoded_graph.decode("utf-8")
            
    
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Some Error Occured", "Error": meta})
    
    try:
        shutil.rmtree('./output/donut/')
    except:
        pass

    return jsonify({"RESPONSE_TYPE": "I", "RESPONSE_MESSAGE":"Scuuess", "DATA":image_base64})

