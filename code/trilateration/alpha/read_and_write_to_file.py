import serial


def main():
    filename = input("""
    What is the name of the file? Make sure it is not a file that already
    exists, this python program does not check this and overrides any
    existing files without confirmation.

    Filename: """)
    f = open(filename, 'w')

    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        while True:
            line = ser.readline()
            line = line.decode('ascii')
            f.write(line + '\n')
            print("Wrote: " + line)


main()
