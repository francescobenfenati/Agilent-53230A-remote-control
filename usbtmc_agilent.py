import usbtmc
import time
import pandas as pd
import logging
log_path='/Users/francescobenfenati/Agilent/Agilent-53230A-remote-control/logs/logfile.log'
data_filename='/Users/francescobenfenati/Agilent/Agilent-53230A-remote-control/data/measurements_{}'
logging.basicConfig(filename=log_path, filemode='a', format='%(message)s')
THRESHOLD = 1*1e-6



df=pd.DataFrame(columns=["time","delay_s"])

def write_data_into_file(dataframe):
    filename=data_filename.format(int(time.time()))
    print("writing dataframe on file {}...".format(filename))
    dataframe.to_csv(filename, mode='a',index=False)
    print("Done!")

#open device. Values obtained with 'lsusb' command or from VISA id
dev = usbtmc.Instrument(idVendor=0x0957,idProduct=0x1907)
#dev = usbtmc.Instrument("USB::2391::6407::MY50002594::0::INSTR")

#get dev identity
#print(dev.ask('*IDN?'))

#configuring
dev.write('CONF:TINT (@1),(@2)') #set time interval measurement between ch1-ch2
dev.write('INP1:COUP DC') #DC coupling
dev.write('INP2:COUP DC')
dev.write('INP1:IMP 50') #impedance set to 50 ohm
dev.write('INP2:IMP 50')
dev.write('INP1:LEV:AUTO OFF')
dev.write('INP2:LEV:AUTO OFF')
dev.write('INP1:LEV .9') #measurement threshold level = 900 mV
dev.write('INP2:LEV .9')

#clear error list
#dev.write('*CLS')

#reset instrument to factory state
#dev.write('*RST')



#polling cycle
while True:
    timestamp = round(time.time(),1)
    delay = float(dev.ask('READ?'))
    if delay > THRESHOLD:
        time_string = "{:.3f}".format(timestamp)
        time_conv = (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp)))+"."+time_string.split(".")[1]
        logging.error(f'{time_conv} - Delay is {delay}. Over threshold!')
        
    df.loc[len(df)+1] = [timestamp,delay]
    if int(timestamp)%30 == 0:
        write_data_into_file(df)
        df = df.iloc[0:0]
    #time.sleep(1)

