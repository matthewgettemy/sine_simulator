""" Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
"""
import time

import numpy as np

from sine import sine
from broker.consumer import consumer
import multiprocessing

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Set up data
N = 200
# x = np.linspace(0, 4*np.pi, N)
# y = np.sin(x)
source = ColumnDataSource(data=dict(x=[], y=[]))
t = time.perf_counter()

# Set up plot
plot = figure(plot_height=400, plot_width=1200, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom,box_zoom")

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

sampling_rate = 50
ten_seconds_data = 10 * sampling_rate
q = multiprocessing.Queue()
p = multiprocessing.Process(
    target=consumer,
    kwargs={
        "topics": ["combine"],
        "broker_address": "localhost:9092",
        "queue": q
    }
)
p.start()

# Set up widgets
text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)


def update_data():
    # t = time.perf_counter()
    # x = np.linspace(1+t, (4*np.pi) + t, N)
    # x = t * 5
    # y = np.sin(x)
    x = []
    y = []
    while not q.empty():
        message = q.get()
        x.extend(message.value["x"])
        y.extend(message.value["y"])
    source.stream(dict(x=x, y=y), rollover=ten_seconds_data)


def widget_update(attrname, old, new):
    t = time.perf_counter()
    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(1+t, (4*np.pi) + t, N)
    y = a*np.sin(k*x + w) + b
    # source.stream(dict(x=x, y=y))
    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', widget_update)


# Set up layouts and add to document
inputs = widgetbox(text, offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
curdoc().add_periodic_callback(update_data, 50)
