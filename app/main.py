import os
import datetime
import sys
from flask import Flask, jsonify


app = Flask(__name__)

# import apps
from api.single_bar import single_bar_graph
from api.multiple_plots import multiple_bar
from api.donut_graph import donut_chart
from api.line_and_bar import line_and_bar_graph

# register blueprints
app.register_blueprint(multiple_bar)
app.register_blueprint(single_bar_graph)
app.register_blueprint(donut_chart)
app.register_blueprint(line_and_bar_graph)


code_update_time = os.getenv("code_update_time", "")


@app.route('/')
def index():
    return "Data Analysis and Visualisation work"


@app.route("/visualization_api/status", methods=['POST', 'GET'])
def server_status():
    """
    returns if server is running or not
    """
    try:
        # removing directory
        date_string = (datetime.datetime.now() + datetime.timedelta(minutes=-15)).strftime("%Y_%m_%d_%H_%M_%S")
        file_to_ignore = ".gitkeep"
        # cleaning output folder
        for i in os.listdir("./output/"):
            if i < date_string and i != file_to_ignore:
                os.remove("./output/" + i)
    except Exception :
        pass
    return jsonify({"status": "running",
                    "message": ["Hello World from Flask in a uWSGI Nginx Docker container with  ",
                                "Python {}.{} (This is data_visualization_work).".format(sys.version_info.major,
                                                                                    sys.version_info.minor),
                                "Updated time: {}".format(code_update_time)]
                    })


if __name__ == '__main__':
    app.run(debug=False)
