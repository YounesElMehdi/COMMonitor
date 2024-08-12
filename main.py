import serial.tools.list_ports


def welcome():
    print('''
    **********************************
    *                                *
    * ╔═╗╔═╗╔╦╗  ┌┬┐┌─┐┌┐┌┬┌┬┐┌─┐┬─┐ *
    * ║  ║ ║║║║  ││││ │││││ │ │ │├┬┘ *
    * ╚═╝╚═╝╩ ╩  ┴ ┴└─┘┘└┘┴ ┴ └─┘┴└─ *
    *                                *
    **********************************
    ''')


def portcheck():
    ports = serial.tools.list_ports.comports()
    print(f"{len(ports)} Ports found")

    if ports:
        for i, port in enumerate(ports, start=1):
            print(f"\nPort {i}:")
            print(f"  Port Name       : {port.name}")
            print(f"  Port PID/VID    : {port.pid}/{port.vid}")
            print(f"  Port HWID       : {port.hwid}")
            print(f"  Port Device     : {port.device}")
            print(f"  Port Product    : {port.product}")
            print(f"  Port Location   : {port.location}")
            print(f"  Port Manufacturer: {port.manufacturer}")
            print(f"  Port Description: {port.description}")
            print(f"  Port Interface  : {port.interface}")
            print(f"  Port Serial No. : {port.serial_number}")
    else:
        print('No Serial Ports Detected')


def ask_for_exit_confirmation():
    while True:
        user_input = input(
            "Do you want to exit the application? Type 'yes' to exit or 'no' to rerun the app: ").strip().lower()
        if user_input == 'yes':
            print("Exiting the application...")
            exit()
        elif user_input == 'no':
            print("Restarting the application...\n")
            main()
        else:
            print("Invalid input. Please type 'yes' to exit or 'no' to rerun the app.")


def main():
    welcome()
    portcheck()
    ask_for_exit_confirmation()


if __name__ == "__main__":
    main()
