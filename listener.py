# vim:ts=4:sts=4:sw=4:et

from mido import Message as Msg
from hue import HuePlay
import mido
import yaml

pad_map = [ 60, 62, 64, 65,
            67, 69, 71, 72,
            74, 76, 77, 79,
            81, 83, 84, 86, ]


class PadScene(object):

    def __init__(self, name, channel=None, pad=None, note=None):
        self.name = name
        self.channel = channel
        self.pad = pad
        self.note = note

    def __repr__(self):
        return "<Scene: \"{}\", Pad {}, Channel {}, Note {}>".format(self.name, self.pad, self.channel, self.note)

class PadSceneLibrary(object):

    scenes = []

    def __init__(self, huelink):
        self.huelink = huelink
        self.huelink.loadScenes()

    def addScene(self, padscene):
        self.scenes.append(padscene)

    def getPads(self):
        return [i.pad for i in self.scenes]

    def removeScene(self, name):
        remove = []
        for i in self.scenes:
            if i.name == name:
                self.scenes.remove(i)

    def setSceneFromPad(self, pad):
        if pad in self.getPads():
            scene = [i for i in self.scenes if i.pad is pad][0]
            self.huelink.setScene(scene.name)

def parseScenes(filename='scenes/scenes.yaml'):
    with open(filename) as f:
        output = yaml.load(f)
    for i in output["scenes"].keys():
        p = PadScene(i)
        p.channel = output["scenes"][i]["channel"]
        p.pad = output["scenes"][i]["pad"]
        p.note = pad_map[p.pad - 1]
        pad_library.addScene(p)


h = HuePlay('10.0.0.211')
m = mido.open_ioport(mido.get_ioport_names()[0])
pad_library = PadSceneLibrary(h)
parseScenes()

while True:
    for i in m.iter_pending():
        if i.type == 'note_on':
            pad_library.setSceneFromPad(pad_map.index(i.note) + 1)
        if i.type == 'control_change':
            if i.control == 12:
                pad_library.huelink.setBrightness(16 * i.value - 1)
            if i.control == 32:
                if pad_library.huelink.toggleLight():
                    l = Msg('control_change', channel=0, control=32, value=127)
                    m.send(l)
            if i.control == 22:
                pad_library.huelink.setCurrent('saturation', 4 * i.value -1)
            if i.control == 14:
                pad_library.huelink.setXValue(i.value, maximum=50)
            if i.control == 15:
                pad_library.huelink.setYValue(i.value, maximum=50)
