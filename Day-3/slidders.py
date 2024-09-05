import dearpygui.dearpygui as dpg

def update_min_value(sender, app_data, user_data):
    min_value = app_data
    current_max = dpg.get_value("anomaly_max_slider")
    dpg.set_value("anomaly_range_text", f"Anomaly Range: {min_value} - {current_max}")

def update_max_value(sender, app_data, user_data):
    max_value = app_data
    current_min = dpg.get_value("anomaly_min_slider")
    dpg.set_value("anomaly_range_text", f"Anomaly Range: {current_min} - {max_value}")

def main():
    dpg.create_context()

    with dpg.window(label="Anomaly Range Interface", width=600, height=400):
        dpg.add_slider_float(label="Min Anomaly Value", default_value=0.0, min_value=0.0, max_value=100.0, callback=update_min_value, tag="anomaly_min_slider")
        dpg.add_slider_float(label="Max Anomaly Value", default_value=100.0, min_value=0.0, max_value=100.0, callback=update_max_value, tag="anomaly_max_slider")
        dpg.add_text("Anomaly Range: 0.0 - 100.0", tag="anomaly_range_text")  # Text widget to display the current range of the sliders

    dpg.create_viewport(title='Anomaly Range Interface', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
