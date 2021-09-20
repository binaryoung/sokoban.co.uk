import pickle
from multiprocessing import Value

from flask import Flask, abort, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

import numpy as np
import torch
from gail_resnet import GAIL
from parallel_env import ParallelEnv

# Init app
app = Flask(__name__, template_folder="static", static_url_path="")

# Init rate limiter
limiter = Limiter(app, key_func=get_ipaddr)

# Load levels
levels = open("storage/levels.pkl", "rb")
levels = pickle.load(levels)

# Load model
model = GAIL()
model.load_state_dict(torch.load("storage/gail.pkl", map_location=torch.device("cpu")))
model.eval()

# Init parallel environments
env = ParallelEnv(10)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/levels/<int:id>")
def get(id):
    if not (0 <= id <= 999):
        abort(404)

    id, room, topology = levels[id]

    return {
        "id": id,
        "room": room.tolist(),
        "topology": topology.tolist(),
    }


@app.route("/api/levels/<int:id>/solve")
@limiter.limit("1/10seconds")
def solve(id):
    if not (0 <= id <= 999):
        abort(404)

    id, room, topology = levels[id]
    room, topology = np.array(room), np.array(topology)

    solved, trajectory = env.solve((id, room, topology), model)

    return {
        "solved": solved,
        "trajectory": trajectory.tolist() if solved == True else []
    }


@app.route("/api/steps")
def get_steps():
    with open("storage/steps.txt", "r") as file:
        steps = int(file.read())

    return {"steps": steps}


@app.route("/api/steps", methods=["PUT", "PATCH"])
def update_steps():
    added_steps = request.form.get("steps", type=int)

    if (added_steps is None) or (not(1 <= added_steps <= 300)):
        abort(400)

    with open("storage/steps.txt", "r+") as file:
        steps = int(file.read())
        file.seek(0)
        file.write(str(steps+added_steps))
        file.truncate()

    return {"status": "success"}
