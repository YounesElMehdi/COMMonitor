import serial
import serial.tools.list_ports
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename=f'COMMonitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_port_info(port, status):
    logging.info(f"Port Name: {port.name}")
    logging.info(f"Port Description: {port.description}")
    logging.info(f"Port Status: {status}")
    logging.info(f"Port Device: {port.device}")
    logging.info(f"Port HWID: {port.hwid}")


def check_port_status(port):
    try:
        with serial.Serial(port.device, timeout=1) as ser:  # Set a 1-second timeout
            status = "Ready to Use"
            print(f"Port {port.name} is {status}.")
            logging.info(f"Port {port.name} is {status}.")

            # Try to read some data, but don't block indefinitely
            received_data = ser.read(100)  # Attempt to read up to 100 bytes
            if received_data:
                logging.info(f"Data received: {received_data}")
            else:
                logging.info("No data received or read timeout occurred.")
    except serial.SerialException as e:
        if isinstance(e, PermissionError) and e.errno == 13:  # ERROR_ACCESS_DENIED
            status = "In Use or Blocked"
        elif isinstance(e, FileNotFoundError) and e.errno == 2:  # ERROR_FILE_NOT_FOUND
            status = "Unavailable/Disabled"
        elif e.errno == 31:  # ERROR_GEN_FAILURE
            status = "Hardware Failure"
        elif e.errno == 1167:  # ERROR_DEVICE_NOT_CONNECTED
            status = "Disconnected"
        elif e.errno == 22:  # ERROR_INVALID_PARAMETER
            status = "Disabled or Invalid Configuration"
        else:
            status = "Unknown Error"

        print(f"Port {port.name} is {status}.")
        logging.error(f"Port {port.name} is {status}. Error: {e}")

    log_port_info(port, status)


def list_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        print(f"{len(ports)} Ports found:")
        for i, port in enumerate(ports, start=1):
            print(f"{i}. {port.name} - {port.description}")
        return ports
    else:
        print("No Serial Ports Detected")
        logging.warning("No Serial Ports Detected")
        return None


def select_and_check_port(ports):
    while True:
        try:
            selection = int(input("Select a port by number to check its status: ").strip())
            selected_port = ports[selection - 1]  # Automatically raises an IndexError if out of range
            check_port_status(selected_port)
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid port number.")
            logging.warning("Invalid selection made by user.")


def ask_for_exit_confirmation():
    while True:
        user_input = input(
            "Do you want to exit the application? Type 'yes' to exit or 'no' to rerun the app: ").strip().lower()

        if user_input in ('yes', 'y'):
            print("Exiting the application...")
            logging.info("User chose to exit the application.")
            exit()
        elif user_input in ('no', 'n'):
            print("Restarting the application...\n")
            logging.info("User chose to rerun the application.")
            main()
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
            logging.warning("User entered invalid input for exit confirmation.")


def main():
    print('''
    **********************************
    *       COMMonitor App           *
    **********************************
    ''')

    logging.info("COMMonitor App Started")

    ports = list_ports()
    if ports:
        select_and_check_port(ports)
    else:
        print("Exiting the application as no ports were detected.")
        logging.info("Exiting the application as no ports were detected.")

    ask_for_exit_confirmation()


if __name__ == "__main__":
    main()
