import pyvisa
import time
rm=pyvisa.ResourceManager()
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

#print(rm.list_resources())
#does not show tcpip interface but nonetheless you can connect to it

#usb interface
#agilent=rm.open_resource('USB0::2391::6407::MY50002594::0::INSTR')

#ethernet interface
agilent = rm.open_resource('TCPIP0::169.254.2.30::inst0::INSTR')

#agilent = rm.open_resource('TCPIP0::169.254.2.30::5025::SOCKET') #does not work
#agilent = rm.open_resource('TCPIP0::A‐53230A‐00050.keysight.com::inst0::INSTR') #does not work


agilent.read_termination = '\n'
agilent.write_termination = '\n'
#print(agilent.query('*IDN?'))

#configuring
agilent.write('CONF:TINT (@1),(@2)') #set time interval measurement between ch1-ch2
agilent.write('INP1:COUP DC') #DC coupling
agilent.write('INP2:COUP DC')
agilent.write('INP1:IMP 50') #impedance set to 50 ohm
agilent.write('INP2:IMP 50')
agilent.write('INP1:LEV:AUTO OFF')
agilent.write('INP2:LEV:AUTO OFF')
agilent.write('INP1:LEV .9') #measurement threshold level = 900 mV
agilent.write('INP2:LEV .9')

#polling cycle
while True:
    timestamp = round(time.time(),1)
    delay = float(agilent.query('READ?'))
    if delay > THRESHOLD:
        time_string = "{:.3f}".format(timestamp)
        time_conv = (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp)))+"."+time_string.split(".")[1]
        logging.error(f'{time_conv} - Delay is {delay}. Over threshold!')

    df.loc[len(df)+1] = [timestamp,delay]
    if int(timestamp)%30 == 0:
        write_data_into_file(df)
        df = df.iloc[0:0]
 
