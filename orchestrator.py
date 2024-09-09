import subprocess
import time
import sys
import toml

def run_component(script_name, config_path):
    return subprocess.Popen([sys.executable, script_name, config_path])

def main():
    with open("cnc_config.toml", "r") as config_file:
        config = toml.load(config_file)

    print(f"Starting orchestrator with controller port {config['ports']['controller']} and emulator port {config['ports']['emulator']}")

    controller = run_component("basic_cnc_controller.py", "cnc_config.toml")
    time.sleep(config['orchestrator']['controller_init_delay']) 

    emulator = run_component("basic_cnc_emulator.py", "cnc_config.toml")
    emulator.wait()
    controller.terminate()
    controller.wait()

    print("Orchestration completed")

if __name__ == "__main__":
    main()

