import serial


def main():
    filename = input("""
    What is the name of the file? Make sure it is not a file that already
    exists, this python program does not check this and overrides any
    existing files without confirmation.

    Filename: """)
    f = open(filename, 'w')
    payload = []

    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        while True:
            line = ser.readline()
            line = line.decode('ascii')
            if (line == "Done\n"):
                write_to_file(f, payload)
                payload = []
            else:
                payload.append(line)


def write_to_file(file, payload):
    line_to_write = ""
    for line in payload:
        line_to_write += line.strip() + ","
    file.write(line_to_write + '\n')
    print("Wrote: " + line_to_write)


main()
