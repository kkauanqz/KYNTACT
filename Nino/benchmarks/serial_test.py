import serial

ser = serial.Serial("/dev/serial0", 9600, timeout=2)
ser.write(b"teste\n")
