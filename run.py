import configparser as cfp
import time

import numpy as np

from modules.StreamWriter import StreamWriter
from modules.StreamReader import StreamReader
from modules.Service import Service
from modules.Source import Source

config = cfp.ConfigParser()
config.read("mixer.cfg")
service = Service(config)

service.print_log('Mixer', 2, 'Starting...')

src_1 = Source(service, config['sources']['s_0'])
src_2 = Source(service, config['sources']['s_1'])
src_3 = Source(service, config['sources']['s_2'])
src_4 = Source(service, config['sources']['s_3'])
src_5 = Source(service, config['sources']['s_4'])
src_6 = Source(service, config['sources']['s_5'])

service.print_log('Mixer', 2, 'Connecting to sources...')
reader_1 = StreamReader(service, src_1).start()
reader_2 = StreamReader(service, src_2).start()
reader_3 = StreamReader(service, src_3).start()
reader_4 = StreamReader(service, src_4).start()
reader_5 = StreamReader(service, src_5).start()
reader_6 = StreamReader(service, src_6).start()
writer = StreamWriter(service)
time.sleep(2)
service.print_log('Mixer', 2, 'Connected (or not)')
start = time.time()
st_int = int(start)
frames = 0
while True:
    frame_1 = reader_1.read()
    frame_2 = reader_2.read()
    frame_3 = reader_3.read()
    frame_4 = reader_4.read()
    frame_5 = reader_5.read()
    frame_6 = reader_6.read()

    buf_1 = np.concatenate((frame_1, frame_2), axis=0)
    buf_2 = np.concatenate((frame_3, frame_4), axis=0)
    buf_3 = np.concatenate((frame_5, frame_6), axis=0)

    buf_4 = np.concatenate((buf_1, buf_2), axis=1)
    buf_5 = np.concatenate((buf_4, buf_3), axis=1)
    end = time.time()
    frames += 1
    fps = frames/(end-start)
    if st_int<int(end):
        service.print_log('Mixer', 0, 'FPS: '+str(int(fps)))
        st_int = int(end)
    writer.write(buf_5)
