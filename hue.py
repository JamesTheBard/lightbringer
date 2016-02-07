# vim:ts=4:sts=4:et:sw=4

from phue import Bridge
import yaml

class HueScene(object):

    def __init__(self, name):
        self.name = name

class HuePlay(object):

    DEFAULT_GROUP = 'Gaming'
    GROUP_LIGHTS = [
        u'RP Lamp 1',
        u'RP Lamp 2',
    ]
    ATTRIBUTES = [ 'on', 'xy', 'saturation', 'brightness', 'transitiontime' ]

    def __init__(self, address):
        self.bridge = Bridge(address)
        self.bridge.connect()
        self.scenes = {}

    def initializeGroups(self, group=DEFAULT_GROUP, lights=GROUP_LIGHTS):
        if self.bridge.get_group(self.DEFAULT_GROUP) is not None:
            self.bridge.delete_group(self.DEFAULT_GROUP)
        self.bridge.create_group(self.DEFAULT_GROUP, self.GROUP_LIGHTS)

    def setScene(self, name):
        if name in self.scenes.keys():
            light_names = self.bridge.get_light_objects('name')
            for light in self.GROUP_LIGHTS:
                light_names[light].on = True
                light_names[light].xy = self.scenes[name].xy
                light_names[light].saturation = self.scenes[name].saturation
                light_names[light].brightness = self.scenes[name].brightness
                self.last_scene = name

    def loadScenes(self, scenefile='scenes/scenes.yaml'):
        with open(scenefile) as f:
            scene_yaml = yaml.load(f)
        for s in scene_yaml["scenes"].keys():
            temp = scene_yaml["scenes"][s]
            scene = HueScene(name=s)
            scene.xy = temp["colors"]
            scene.saturation = temp["saturation"]
            scene.brightness = temp["brightness"]
            self.scenes[s] = scene

    def setCurrent(self, attribute, value, transition=None):
        if attribute in self.ATTRIBUTES:
            light_names = self.bridge.get_light_objects('name')
            for light in self.GROUP_LIGHTS:
                tt = light_names[light].transitiontime
                light_names[light].transitiontime = 1
                setattr(light_names[light], attribute, value)
                light_names[light].transitiontime = tt

    def setBrightness(self, value):
        light_names = self.bridge.get_light_objects('name')
        for light in self.GROUP_LIGHTS:
            tt = light_names[light].transitiontime
            light_names[light].transitiontime = 1 
            light_names[light].brightness = value
            light_names[light].transitiontime = tt

    def setXValue(self, value, maximum=127):
        light_names = self.bridge.get_light_objects('name')
        for light in self.GROUP_LIGHTS:
            xvalue = float(value)/maximum
            yvalue = light_names[light].xy[1]
            light_names[light].xy = (xvalue, yvalue)
         
    def setYValue(self, value, maximum=127):
        light_names = self.bridge.get_light_objects('name')
        for light in self.GROUP_LIGHTS:
            yvalue = float(value)/maximum
            xvalue = light_names[light].xy[1]
            light_names[light].xy = (xvalue, yvalue)

    def toggleLight(self):
        light_names = self.bridge.get_light_objects('name')
        for light in self.GROUP_LIGHTS:
            tt = light_names[light].transitiontime
            light_names[light].transitiontime = 4 
            light_names[light].on ^= True
            light_names[light].transitiontime = tt
        return light_names[light].on
