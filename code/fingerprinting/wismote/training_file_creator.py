import sys
import serial


def main():
    f = open(sys.argv[1], 'a')
    f.write('c' + sys.argv[2] + ' ' + sys.argv[3] + '\n')
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
