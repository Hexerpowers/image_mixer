import configparser as cfp
import time

import numpy as np

from modules.MjpegStreamReader import MjpegStreamReader
from modules.StreamWriter import StreamWriter
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
reader_1 = MjpegStreamReader(service, src_1).start()
reader_2 = MjpegStreamReader(service, src_2).start()
reader_3 = MjpegStreamReader(service, src_3).start()
reader_4 = MjpegStreamReader(service, src_4).start()
reader_5 = MjpegStreamReader(service, src_5).start()
reader_6 = MjpegStreamReader(service, src_6).start()
writer = StreamWriter(service)
time.sleep(2)
service.print_log('Mixer', 2, 'Connected (or not)')
start = time.time()
st_int = int(start)
frames = 0
writer.start()


def concat(frame_1, frame_2, frame_3, frame_4, frame_5, frame_6):
    return np.vstack(
        (np.hstack((np.hstack((frame_1, frame_2)), frame_3)), np.hstack((np.hstack((frame_4, frame_5)), frame_6))))


while True:

    writer.write(
        concat(reader_1.read(), reader_2.read(), reader_3.read(), reader_4.read(), reader_5.read(), reader_6.read()))

    end = time.time()
    frames += 1
    fps = frames / (end - start)
    if st_int < int(end):
        service.print_log('Mixer', 0, 'Current IPS: ' + str(int(fps)))
        st_int = int(end)
