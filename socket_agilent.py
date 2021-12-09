import time, socket
import pandas as pd
import logging
logging.basicConfig(filename='/Users/francescobenfenati/agilent/logs/logfile.log', filemode='a', format='%(message)s')
THRESHOLD = 1*1e-6

df=pd.DataFrame(columns=["time","delay(s)"])

def write_data_into_file(dataframe):
    filename="/Users/francescobenfenati/agilent/data/measurements_{}".format(int(time.time()))
    print("writing dataframe on file {}...".format(filename))
    dataframe.to_csv(filename, mode='a',index=False)
    print("Done!")


# Define socket type as stream, allowing a port number to be defined
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to product's IP address address at default 50505 socket
s.connect(('169.254.2.30', 5025))

# Send SCPI command requesting the product to identify itself
#s.sendall('*IDN?\n'.encode())
# Receive the product's response and display it in the terminal
#print(s.recv(1024).decode())

# Send SCPI command to read measurement
#polling cycle
while True:
    timestamp = round(time.time(),1)
    s.sendall('READ?\n'.encode())
    delay = float(s.recv(1024).decode())
    if delay > THRESHOLD:
        time_string = "{:.3f}".format(timestamp)
        time_conv = (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp)))+"."+time_string.split(
".")[1]
        logging.error(f'{time_conv} - Delay is {delay}. Over threshold!')

    df.loc[len(df)+1] = [timestamp,delay]
    if int(timestamp)%30 == 0:
        write_data_into_file(df)
        df = df.iloc[0:0]

# Close the communication channel to the product
s.close()
