from flask import Flask
import time
import os
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

serverapp = Flask(__name__)
syncfile = "/tmp/toxic-{}.time".format(os.getpid())

@serverapp.route("/", methods=["GET"])
def index():
    if not serverapp.config["secret"]:
        open(syncfile, "w").write(str(time.time()))
        return "", 200
    else:
        return "", 403

@serverapp.route("/<secret>", methods=["GET"])
def secret(secret):
    if not serverapp.config["secret"] or secret == serverapp.config["secret"]:
        open(syncfile, "w").write(str(time.time()))
        return "", 200
    else:
        return "", 403

def handle_connection(timeout, command, pre=None):
    connection_established = False
    while True:
        time.sleep(1)
        if os.path.isfile(syncfile):
            if not connection_established:
                if pre:
                    os.system(pre)
                connection_established = True
            with open(syncfile, "r") as f:
                last_con = int(time.time()) - int(float(f.read()))
                if last_con >= timeout:
                    os.system(command)
                    os.remove(syncfile)
                    connection_established = False
