#load:Train:
from uasyncio import sleep_ms
import os

class selective:
    def __init__(self, control):
        self.confpath = control.profile_folder+'/light/train.conf'
        self.Control = control
        self.isenable = False
        self.color = [127,127,127]
        self.oldcolor = [0, 0, 0]

    async def start(self):
        self.isenable = True
        leds = self.Control.redata['!np_leds']
        led = 0
        while self.isenable:
            if not self.color == self.oldcolor:
                self.oldcolor = self.color
            
            self.Control.np.fill((0,0,0))
            for add in range(self.Control.redata['!leds_selected']):
                self.Control.np[leds-(abs(leds-(led-add)))-1] = self.color
                
            if self.Control.redata['!isenable']:
                if self.Control.redata['!rotation_led_reverse']:
                    led -= 1
                else:
                    led += 1
                if led > leds-1:
                    led = 0
                elif led < 0:
                    led = leds
            
            self.Control.np.write()
            await sleep_ms(self.Control.redata['!delay_change'])

    def __light_set(self, type_data, data):
        if type_data == 'monocolor':
            splitdata = data.split(',')
            self.color = [int(splitdata[0]),int(splitdata[1]),int(splitdata[2])]
            self.Control.redata['!r_c'] = self.color[0]
            self.Control.redata['!g_c'] = self.color[1]
            self.Control.redata['!b_c'] = self.color[2]
        elif type_data == 'leds':
            self.Control.redata['!leds_selected'] = int(data)
        elif type_data == 'delay':
            self.Control.redata['!delay_change'] = int(data)
        elif type_data == 'isenable':
            self.Control.redata['!isenable'] = data == 'true'
        elif type_data == 'led_reverse':
            self.Control.redata['!rotation_led_reverse'] = data == 'true'
        self.Control.writefile(self.confpath,
                       'r_c:'+str(self.Control.redata['!r_c'])+'\n'+
                       'g_c:'+str(self.Control.redata['!g_c'])+'\n'+
                       'b_c:'+str(self.Control.redata['!b_c'])+'\n'+
                       'leds_selected:'+str(self.Control.redata['!leds_selected'])+'\n'+
                       'delay_change:'+str(self.Control.redata['!delay_change'])+'\n'+
                       'isenable:'+str(self.Control.redata['!isenable'])+'\n'+
                       'rotation_led_reverse:'+str(self.Control.redata['!rotation_led_reverse'])+'\n')
            

    async def __callback(self, request):
        await self.Control.sendfile(request, '/profiles/light/','train.web')

    def addparametrs(self):
        self.Control.light_callback = self.__callback
        self.Control.light_set = self.__light_set
        self.Control.redata['!r_c'] = self.color[0]
        self.Control.redata['!g_c'] = self.color[1]
        self.Control.redata['!b_c'] = self.color[2]
        self.Control.redata['!np_leds'] = len(self.Control.np)
        self.Control.redata['!leds_selected'] = 3
        self.Control.redata['!delay_change'] = 20
        self.Control.redata['!isenable'] = True
        self.Control.redata['!rotation_led_reverse'] = False

        if not 'train.conf' in os.listdir(self.Control.profile_folder+'/light/'):
            open(self.confpath,'x').close()
        file = open(self.confpath)
        while True:
            line = file.readline()
            if not line:
                break
            read = line.split(':')
            if len(read) > 1:
                if  read[0] == 'r_c':
                    self.Control.redata['!r_c'] = int(read[1][:-1])
                elif read[0] == 'g_c':
                    self.Control.redata['!g_c'] = int(read[1][:-1])
                elif read[0] == 'b_c':
                    self.Control.redata['!b_c'] = int(read[1][:-1])
                elif read[0] == 'leds_selected':
                    self.Control.redata['!leds_selected'] = int(read[1][:-1])
                elif read[0] == 'delay_change':
                    self.Control.redata['!delay_change'] = int(read[1][:-1])
                elif read[0] == 'isenable':
                    self.Control.redata['!isenable'] = read[1][:-1] == 'True'
                elif read[0] == 'rotation_led_reverse':
                    self.Control.redata['!rotation_led_reverse'] = read[1][:-1] == 'True'
        file.close()
        self.color = [self.Control.redata['!r_c'],self.Control.redata['!g_c'],self.Control.redata['!b_c']]

    def removeparametrs(self):
        self.Control.light_callback = None
        self.Control.light_set = None
        self.Control.redata.pop('!r_c', None)
        self.Control.redata.pop('!g_c', None)
        self.Control.redata.pop('!b_c', None)
        self.Control.redata.pop('!np_leds_selected', None)
        self.Control.redata.pop('!delay_change', None)
        self.Control.redata.pop('!isenable', None)
        self.Control.redata.pop('rotation_led_reverse', None)

    def stop(self):
        self.isenable = False
        self.oldcolor = [0, 0, 0]
        self.Control.np.fill((0, 0, 0))
        self.Control.np.write()

def create(p):
    return selective(p)
