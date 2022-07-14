import os
import threading
import time
from minipupper import CONF
from flask import Flask, send_from_directory
from backend.controller.wobble import Wobble
from backend.controller.walk import Walk

if CONF.minipupper.environment == 'simulator':
    from backend.controller.simulator.hardware_interface import Servo
else:
    from backend.controller.pupper.hardware_interface import Servo

app = Flask(__name__)
if CONF.minipupper.environment == 'simulator':
    pid = os.spawnv(os.P_NOWAIT, "%s/bin/minipupper-sim" % os.environ['VIRTUAL_ENV'], ["dummy"])
    time.sleep(1)
hardware_interface = Servo()
wobble_controller = Wobble(hardware_interface)
walk_controller = Walk(hardware_interface)
current = 'wobble'


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static/', path)


@app.route('/')
@app.route('/wobble')
@app.route('/walk')
@app.route('/trot')
@app.route('/gallop')
def root():
    return send_from_directory("%s%s" % (os.path.dirname(__file__), '/static/'), 'index.html')


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory("%s%s" % (os.path.dirname(__file__), '/img/'), path)


@app.route("/wobble/<string:command>/<string:param>", methods=['GET'])
def wobble(command, param):
    wobble_controller.setParams('wobble', command, param)
    return wobble_controller.getParams('wobble', command, param)


@app.route("/walk/<string:command>/<string:param>", methods=['GET'])
def walk(command, param):
    gait = 'walk'
    walk_controller.setParams(gait, command, param)
    return walk_controller.getParams(gait, command, param)


@app.route("/trot/<string:command>/<string:param>", methods=['GET'])
def trot(command, param):
    gait = 'trot'
    walk_controller.setParams(gait, command, param)
    return walk_controller.getParams(gait, command, param)


@app.route("/gallop/<string:command>/<string:param>", methods=['GET'])
def gallop(command, param):
    gait = 'gallop'
    walk_controller.setParams(gait, command, param)
    return walk_controller.getParams(gait, command, param)


def runLoop():
    while True:

        if wobble_controller.getAciveState():
            wobble_controller.execute()
        else:
            walk_controller.execute()


def main():
    threading.Thread(target=runLoop, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()
