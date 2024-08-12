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
    print(len(ports), 'ports found')
    if ports:
        for port in ports:
            print(port.name)
            print(port.pid)
            print(port.hwid)
            print(port.device)
            print(port.product)
            print(port.location)
            print(port.manufacturer)
            print(port.description)
            print(port.interface)
            print(port.serial_number)
            print(port.vid)
    else:
        print('No Seria port Detected')


def ask_for_exit_confirmation():
    while True:
        user_input = input("Do you want to exit the application? Type 'yes' to exit or 'no' to rerun the app: ").strip().lower()
        if user_input == 'yes':
            print("Exiting the application...")
            break
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
