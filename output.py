import mido
from mido import Message as M

m_out = mido.open_ioport(mido.get_ioport_names()[0])

while True:
    for i in m_out.iter_pending():
        print i
