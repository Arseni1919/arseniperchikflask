# app.py
from flask import Flask, request, jsonify, render_template, url_for, redirect
import pandas as pd
from threading import Thread
import time


app = Flask(__name__)


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/config')
def config_func():
    for k in app.config:
        print(f'{k}')
    print(type(app.config))
    return 'done'


@app.route('/thread')
def threaded_task(duration):
    for i in range(duration):
        print("Working... {}/{}".format(i + 1, duration))
        time.sleep(1)
    return 'aaa'


@app.route("/task/", defaults={'duration': 5})
@app.route("/task/<int:duration>")
def task_func(duration):
    thread = Thread(target=threaded_task, args=(duration,))
    thread.daemon = True
    thread.start()
    return jsonify({'thread_name': str(thread.name),
                    'started': True})


@app.route('/data')
def data():
    new = pd.read_csv('static/data/real_data_2days_sample.csv')
    # query = pd.DataFrame(json_vector)
    data_dict = {}
    for stock in new:
        data_dict[stock] = new[stock].values
        print(data_dict[stock].shape)
    return render_template('data.html', data=data_dict)


# A welcome message to test our server
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    # app.run(threaded=True, port=5000)
    app.run(debug=True)
    app.run()