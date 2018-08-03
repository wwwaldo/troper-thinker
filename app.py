from flask import Flask, render_template, send_file
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from src import Scorer


# import pdb; pdb.set_trace()
sc = Scorer("./src/store.p")
app = Flask(__name__)


@app.route('/')
def start():
    return 'This will be the entry page'

@app.route('/<path:namespace>/<path:media>/plot.png')
def image(namespace, media):
    # make a plot, export as png and return that image at this address
    fig = plt.figure()
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/<path:namespace>/<path:media>')
def results(namespace, media):
    arr = np.zeros((3,3))
    ploturl = f"/{namespace}/{media}/plot.png"

    return render_template('hello.html', namespace=namespace, media=sc.ls(), ploturl=ploturl)
