from io_utils import load_csv_data, save_selected_data, update_json_register

def process_csv_interactive(filename, xcol="time", ycol="force", json_log="assessments_register.json"):
    from gui import launch_gui_assessment
    return launch_gui_assessment(filename, xcol, ycol, json_log)
