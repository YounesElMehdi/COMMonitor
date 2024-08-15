import serial
import serial.tools.list_ports
import sys
import logging
import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize Colorama for cross-platform colored text
init()

# Load configuration from JSON file
with open('app_config.json', 'r') as config_file:
    config = json.load(config_file)

# Set the terminal size
sys.stdout.write(f"\x1b[8;{config['terminal_size']['height']};{config['terminal_size']['width']}t")

# Set up logging
log_filename = f"{config['log_settings']['log_filename']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=getattr(logging, config['log_settings']['log_level']),
    format=config['log_settings']['log_format'],
    datefmt=config['log_settings']['log_date_format']
)


def welcome():
    print(Fore.CYAN + '''
    **********************************
    *       Welcome to COMMonitor    *
    **********************************
    * Version: 2.0                   *
    * Developed for offline stations *
    * Diagnose and test serial ports *
    *                                *
    * Developer: Yelmehdi            *
    **********************************
    ''' + Style.RESET_ALL)
    logging.info("COMMonitor App Started")


def main_menu():
    print(Fore.YELLOW + '''
    Main Menu:
    1. List and Check COM Ports
    2. Perform Stress Test
    3. Perform Loopback Test
    4. Error Code Lookup
    5. Run Basic Diagnostic Script
    6. Exit Application
    ''' + Style.RESET_ALL)
    logging.info("Displayed Main Menu")


def list_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        print(f"{len(ports)} Ports found:")
        for i, port in enumerate(ports, start=1):
            print(f"{i}. {port.name} - {port.description}")
        return ports
    else:
        print(Fore.RED + "No Serial Ports Detected" + Style.RESET_ALL)
        logging.warning("No Serial Ports Detected")
        return None


def check_port_status(port):
    try:
        with serial.Serial(port.device, timeout=1) as ser:
            status = "Ready to Use"
            print(Fore.GREEN + f"Port {port.name} is {status}." + Style.RESET_ALL)
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

        print(Fore.RED + f"Port {port.name} is {status}." + Style.RESET_ALL)
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
            print(Fore.YELLOW + f"Starting stress test on {port.name} for {duration} seconds..." + Style.RESET_ALL)
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
                print(Fore.GREEN + f"Stress test passed for {port.name}. No errors detected." + Style.RESET_ALL)
                logging.info(f"Stress test passed for {port.name}. No errors detected.")
            else:
                print(Fore.RED + f"Stress test failed for {port.name}. {errors} errors detected." + Style.RESET_ALL)
                logging.error(f"Stress test failed for {port.name}. {errors} errors detected.")
    except serial.SerialException as e:
        print(Fore.RED + f"Error during stress test on {port.name}: {e}" + Style.RESET_ALL)
        logging.error(f"Error during stress test on {port.name}: {e}")


def loopback_test(port):
    try:
        with serial.Serial(port.device, timeout=1) as ser:
            test_data = b'LOOPBACK_TEST'
            print(Fore.YELLOW + f"Performing loopback test on {port.name}..." + Style.RESET_ALL)
            logging.info(f"Performing loopback test on {port.name}...")

            ser.write(test_data)
            received_data = ser.read(len(test_data))

            if received_data == test_data:
                print(Fore.GREEN + f"Loopback test passed for {port.name}. Data matched." + Style.RESET_ALL)
                logging.info(f"Loopback test passed for {port.name}. Data matched.")
            else:
                print(Fore.RED + f"Loopback test failed for {port.name}. Data did not match." + Style.RESET_ALL)
                logging.error(f"Loopback test failed for {port.name}. Data did not match.")
    except serial.SerialException as e:
        print(Fore.RED + f"Error during loopback test on {port.name}: {e}" + Style.RESET_ALL)
        logging.error(f"Error during loopback test on {port.name}: {e}")


def error_code_lookup():
    print(Fore.YELLOW + "Error Code Lookup" + Style.RESET_ALL)
    while True:
        try:
            code = int(input("Enter the error code you want to look up (or type 0 to return to the Main Menu): ").strip())
            if code == 0:
                break
            description = config['error_codes'].get(str(code), "Error code not recognized.")
            print(Fore.CYAN + f"Error Code {code}: {description}" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid error code." + Style.RESET_ALL)


def run_diagnostic_script():
    print(Fore.YELLOW + "Running Basic Diagnostic Script..." + Style.RESET_ALL)
    try:
        ports = list_ports()
        if ports:
            for port in ports:
                check_port_status(port)
        print(Fore.GREEN + "Diagnostic script completed." + Style.RESET_ALL)
        logging.info("Basic diagnostic script completed.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while running the diagnostic script: {e}" + Style.RESET_ALL)
        logging.error(f"An error occurred while running the diagnostic script: {e}")


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
            print(Fore.RED + "Invalid selection. Please enter a valid port number." + Style.RESET_ALL)
            logging.warning("Invalid selection made by user.")


def ask_for_exit_confirmation():
    while True:
        user_input = input(
            "Do you want to exit the application? Type 'yes' to exit or 'no' to return to the Main Menu: ").strip().lower()

        if user_input in ('yes', 'y'):
            print(Fore.YELLOW + "Exiting the application..." + Style.RESET_ALL)
            logging.info("User chose to exit the application.")
            exit()
        elif user_input in ('no', 'n'):
            print(Fore.GREEN + "Returning to the Main Menu...\n" + Style.RESET_ALL)
            logging.info("User chose to return to the Main Menu.")
            main_menu_handler()
        else:
            print(Fore.RED + "Invalid input. Please type 'yes' or 'no'." + Style.RESET_ALL)
            logging.warning("User entered invalid input for exit confirmation.")


def main_menu_handler():
    welcome()
    while True:
        main_menu()
        try:
            choice = int(input("Enter your choice (1-6): ").strip())
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
                error_code_lookup()
            elif choice == 5:
                run_diagnostic_script()
            elif choice == 6:
                ask_for_exit_confirmation()
            else:
                print(Fore.RED + "Invalid choice. Please enter a number between 1 and 6." + Style.RESET_ALL)
                logging.warning("Invalid menu choice made by user.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
            logging.warning("Invalid input for menu choice.")


if __name__ == "__main__":
    main_menu_handler()
