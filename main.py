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


def welcome():
    print('''
    **********************************
    *       Welcome to COMMonitor    *
    **********************************
    * Version: 1.0                   *
    * Developed for offline stations *
    * Diagnose and test serial ports *
    **********************************
    ''')
    logging.info("COMMonitor App Started")


def main_menu():
    print('''
    Main Menu:
    1. List and Check COM Ports
    2. Perform Stress Test
    3. Perform Loopback Test
    4. Exit Application
    ''')
    logging.info("Displayed Main Menu")


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


def check_port_status(port):
    try:
        with serial.Serial(port.device, timeout=1) as ser:
            status = "Ready to Use"
            print(f"Port {port.name} is {status}.")
            logging.info(f"Port {port.name} is {status}.")

            received_data = ser.read(100)
            if received_data:
                logging.info(f"Data received: {received_data}")
            else:
                logging.info("No data received or read timeout occurred.")
    except serial.SerialException as e:
        if isinstance(e, PermissionError) and e.errno == 13:
            status = "In Use or Blocked"
        elif isinstance(e, FileNotFoundError) and e.errno == 2:
            status = "Unavailable/Disabled"
        elif e.errno == 31:
            status = "Hardware Failure"
        elif e.errno == 1167:
            status = "Disconnected"
        elif e.errno == 22:
            status = "Disabled or Invalid Configuration"
        else:
            status = "Unknown Error"

        print(f"Port {port.name} is {status}.")
        logging.error(f"Port {port.name} is {status}. Error: {e}")

    log_port_info(port, status)


def log_port_info(port, status):
    logging.info(f"Port Name: {port.name}")
    logging.info(f"Port Description: {port.description}")
    logging.info(f"Port Status: {status}")
    logging.info(f"Port Device: {port.device}")
    logging.info(f"Port HWID: {port.hwid}")


def port_stress_test(port, duration=10):
    try:
        with serial.Serial(port.device, timeout=1) as ser:
            start_time = datetime.now()
            print(f"Starting stress test on {port.name} for {duration} seconds...")
            logging.info(f"Starting stress test on {port.name} for {duration} seconds.")

            data_to_send = b'0123456789ABCDEF' * 64
            errors = 0
            while (datetime.now() - start_time).seconds < duration:
                ser.write(data_to_send)
                received_data = ser.read(len(data_to_send))
                if received_data != data_to_send:
                    errors += 1
                    logging.warning(f"Data mismatch detected on {port.name}.")

            if errors == 0:
                print(f"Stress test passed for {port.name}. No errors detected.")
                logging.info(f"Stress test passed for {port.name}. No errors detected.")
            else:
                print(f"Stress test failed for {port.name}. {errors} errors detected.")
                logging.error(f"Stress test failed for {port.name}. {errors} errors detected.")
    except serial.SerialException as e:
        print(f"Error during stress test on {port.name}: {e}")
        logging.error(f"Error during stress test on {port.name}: {e}")


def loopback_test(port):
    try:
        with serial.Serial(port.device, timeout=1) as ser:
            test_data = b'LOOPBACK_TEST'
            print(f"Performing loopback test on {port.name}...")
            logging.info(f"Performing loopback test on {port.name}...")

            ser.write(test_data)
            received_data = ser.read(len(test_data))

            if received_data == test_data:
                print(f"Loopback test passed for {port.name}. Data matched.")
                logging.info(f"Loopback test passed for {port.name}. Data matched.")
            else:
                print(f"Loopback test failed for {port.name}. Data did not match.")
                logging.error(f"Loopback test failed for {port.name}. Data did not match.")
    except serial.SerialException as e:
        print(f"Error during loopback test on {port.name}: {e}")
        logging.error(f"Error during loopback test on {port.name}: {e}")


def select_port_for_test(ports, test_type):
    while True:
        try:
            selection = int(input(f"Select a port by number to {test_type}: ").strip())
            selected_port = ports[selection - 1]  # Automatically raises an IndexError if out of range
            if test_type == "check status":
                check_port_status(selected_port)
            elif test_type == "perform stress test":
                port_stress_test(selected_port)
            elif test_type == "perform loopback test":
                loopback_test(selected_port)
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid port number.")
            logging.warning("Invalid selection made by user.")


def ask_for_exit_confirmation():
    while True:
        user_input = input(
            "Do you want to exit the application? Type 'yes' to exit or 'no' to return to the Main Menu: ").strip().lower()

        if user_input in ('yes', 'y'):
            print("Exiting the application...")
            logging.info("User chose to exit the application.")
            exit()
        elif user_input in ('no', 'n'):
            print("Returning to the Main Menu...\n")
            logging.info("User chose to return to the Main Menu.")
            main_menu_handler()
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
            logging.warning("User entered invalid input for exit confirmation.")


def main_menu_handler():
    welcome()
    while True:
        main_menu()
        try:
            choice = int(input("Enter your choice (1-4): ").strip())
            if choice == 1:
                ports = list_ports()
                if ports:
                    select_port_for_test(ports, "check status")
            elif choice == 2:
                ports = list_ports()
                if ports:
                    select_port_for_test(ports, "perform stress test")
            elif choice == 3:
                ports = list_ports()
                if ports:
                    select_port_for_test(ports, "perform loopback test")
            elif choice == 4:
                ask_for_exit_confirmation()
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                logging.warning("Invalid menu choice made by user.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            logging.warning("Invalid input for menu choice.")


if __name__ == "__main__":
    main_menu_handler()
