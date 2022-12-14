"""

"""

import time
import numpy as np
from broker.consumer import consumer
import multiprocessing
from scipy.fftpack import fft
from scipy.fftpack import fftfreq

from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


def start_consuming(q: multiprocessing.Queue):

    consumer_process = multiprocessing.Process(
        target=consumer,
        kwargs={
            "topics": ["sine", "combine", "fft"],
            "broker_address": "localhost:9092",
            "queue": q
        }
    )
    consumer_process.start()


consumer_queue = multiprocessing.Queue()
start_consuming(consumer_queue)

sine_figure = figure(
    plot_height=250,
    plot_width=1200,
    title="sine waves",
    tools="pan,wheel_zoom,box_zoom,reset"
)
combined_figure = figure(
    plot_height=250,
    plot_width=1200,
    title="combined waves",
    tools="pan,wheel_zoom,box_zoom,reset"
)
spectrum_figure = figure(
    plot_height=250,
    plot_width=1200,
    title="waves spectrum",
    tools="pan,wheel_zoom,box_zoom,reset"
)

sine_data = ColumnDataSource({"x": [], "y": []})
combined_data = ColumnDataSource({"x": [], "y": []})
spectrum_data = ColumnDataSource({"x": [], "y": []})
source_map = {
    "sine": sine_data,
    "combine": combined_data,
    "fft": spectrum_data
}

sine_figure.scatter(
    x="x",
    y="y",
    source=sine_data,
    color="red"
)
combined_figure.line(
    x="x",
    y="y",
    source=combined_data,
    color="red"
)
spectrum_figure.line(
    x="x",
    y="y",
    source=spectrum_data,
    color="blue"
)


def update_data():
    data = {}
    # while not consumer_queue.empty():
    message = consumer_queue.get()
    topic = message.topic
    if topic in data:
        data[topic]["x"].extend(message.value["x"])
        data[topic]["y"].extend(message.value["y"])
    else:
        data[topic] = {"x": message.value["x"], "y": message.value["y"]}

    for topic in data:
        source = source_map[topic]
        if topic == "sine":
            source.stream(dict(data[topic]), rollover=2250)
        elif topic == "combine":
            source.stream(dict(data[topic]), rollover=750)
        elif topic == "fft":
            source.data = dict(data[topic])




curdoc().add_root(gridplot([[sine_figure], [combined_figure], [spectrum_figure]]))
curdoc().title = "Waves"
curdoc().add_periodic_callback(update_data, 10)
