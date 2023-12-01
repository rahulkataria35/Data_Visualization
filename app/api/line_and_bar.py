import traceback
from flask import Blueprint, request, jsonify
import shutil
import os
from common.common import get_random_dir_file_name, image_to_base64
from utils.plots import single_line_or_bar_graph

line_and_bar_graph = Blueprint('line_and_bar_graph', __name__, url_prefix='/visualization_api')

@line_and_bar_graph.route("/line_and_bar", methods= ['POST'])
def line_and_bar():
    try:
        input_data = request.get_json()
        print("input_data==", input_data)
    except Exception as e:
        return jsonify(
            {"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Unable to get data", "Error": str(e)})
    
    
    # save file into folder
    name = get_random_dir_file_name(prefix="", suffix="doc")
    path = "./output/line/" + str(name)

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    try:
        line_bar_response = single_line_or_bar_graph(input_data, path)
        try:
            if line_bar_response["RESPONSE_TYPE"] == "E":
                return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Mandatory Keys Missing", "Error": line_bar_response['Error']})
        except:
            encoded_graph = image_to_base64(line_bar_response)
            image_base64 = encoded_graph.decode("utf-8")
            
    
    except Exception as ex:
        meta = {
            'exc_type': type(ex).__name__,
            'exc_message': traceback.format_exc().split('\n')
        }
        return jsonify({"RESPONSE_TYPE": "E", "RESPONSE_MESSAGE": "Some Error Occured", "Error": meta})
    
    try:
        shutil.rmtree('./output/line/')
    except:
        pass

    return jsonify({"RESPONSE_TYPE": "I", "RESPONSE_MESSAGE":"Scuuess", "DATA":image_base64})




