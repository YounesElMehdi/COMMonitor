import serial.tools.list_ports
import serial

def display_welcome_message():
    print('''
    **********************************
    *                                *
    * ╔═╗╔═╗╔╦╗  ┌┬┐┌─┐┌┐┌┬┌┬┐┌─┐┬─┐ *
    * ║  ║ ║║║║  ││││ │││││ │ │ │├┬┘ *
    * ╚═╝╚═╝╩ ╩  ┴ ┴└─┘┘└┘┴ ┴ └─┘┴└─ *
    *                                *
    **********************************
    ''')


def list_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        print(f"{len(ports)} Ports found:")
        for i, port in enumerate(ports, start=1):
            print(f"{i}. {port.name} - {port.description}")
        return ports
    else:
        print("No Serial Ports Detected")
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


def check_port_status(port):
    try:
        with serial.Serial(port.device):
            print(f"Port {port.name} is Available.")
    except serial.SerialException:
        print(f"Port {port.name} is In Use or Unavailable.")


def main():
    display_welcome_message()
    ports = list_ports()
    if ports:
        select_and_check_port(ports)
    else:
        print("Exiting the application as no ports were detected.")


if __name__ == "__main__":
    main()
