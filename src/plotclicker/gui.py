import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io_utils import load_csv_data, save_selected_data, update_json_register
import os

def draw_figure(canvas_elem, figure):
    canvas = FigureCanvasTkAgg(figure, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
    return canvas

def launch_gui_assessment(csv_filename, xcol="time", ycol="force", json_log="assessments_register.json"):
    data, x_col, y_col = load_csv_data(csv_filename, xcol, ycol)
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'], label="Raw Data")
    ax.set(title=f"{x_col} vs {y_col}", xlabel=x_col, ylabel=y_col)
    ax.grid(True)

    crosshair, = ax.plot([], [], 'ro', label='Selected', markersize=8)
    selected = []

    layout = [
        [sg.Canvas(key='-CANVAS-', size=(640, 480), expand_x=True, expand_y=True)],
        [sg.Button("Save & Close"), sg.Button("Cancel")]
    ]

    window = sg.Window("Data Assessor", layout, finalize=True)
    canvas = draw_figure(window['-CANVAS-'], fig)
    window['-CANVAS-'].expand(True, True)

    def onclick(event):
        if event.xdata is None or event.ydata is None:
            return
        selected.append((event.xdata, event.ydata))
        xs, ys = zip(*selected)
        crosshair.set_data(xs, ys)
        fig.canvas.draw()

    fig.canvas.mpl_connect('button_press_event', onclick)

    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "Save & Close":
            assessed_file, assess_id = save_selected_data(
                selected, data, x_col, y_col, os.path.basename(csv_filename)
            )
            register_entry = {
                "assessment_id": assess_id,
                "raw_filename": csv_filename,
                "assessed_filename": assessed_file,
                "x_col": x_col,
                "y_col": y_col
            }
            update_json_register(json_log, register_entry)
            break
    window.close()
    return assessed_file
