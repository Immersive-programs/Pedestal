#load:Default:
from uasyncio import sleep_ms
class default:
    def __init__(self, control):
        self.confpath = control.profile_folder+'/rotation/default.conf'
        self.Control = control
        self.isenable = False

    async def start(self):
        self.isenable = True
        self.Control.rst.value(1)
        if not self.Control.redata['!pwm_f'] == 0:
            self.Control.rst.value(1)
            self.Control.pwm.duty(512)

    def __set(self, type_data, data):
        if type_data == 'frequency':
            self.Control.redata['!pwm_f'] = int(data)
            if not data == '0' and self.isenable:
                self.Control.rst.value(1)
                self.Control.pwm.freq(self.Control.redata['!pwm_f'])
            else:
                self.Control.rst.value(0)
        elif type_data == 'reverse':
            self.Control.redata['!rotation_reverse'] = data == 'true'
            self.Control.dir.value(self.Control.redata['!rotation_reverse'])
        elif type_data == 'divider':
            steps = int(data)
            self.Control.redata['!steps'] = steps
            self.setdivider(steps)
        self.Control.writefile(self.confpath,
        'frequency:'+str(self.Control.redata['!pwm_f'])+'\n'+
        'reverse:'+str(self.Control.redata['!rotation_reverse'])+'\n'+
        'steps:'+str(self.Control.redata['!steps'])+'\n')

    async def __callback(self, request):
        await self.Control.sendfile(request, '/profiles/rotation/','default.web')
        
    def setdivider(self, steps):
        if   steps == 0:
            self.Control.m0.value(0)
            self.Control.m1.value(0)
            self.Control.m2.value(0)
        elif steps == 1:
            self.Control.m0.value(1)
            self.Control.m1.value(0)
            self.Control.m2.value(0)
        elif steps == 2:
            self.Control.m0.value(0)
            self.Control.m1.value(1)
            self.Control.m2.value(0)
        elif steps == 3:
            self.Control.m0.value(1)
            self.Control.m1.value(1)
            self.Control.m2.value(0)
        elif steps == 4:
            self.Control.m0.value(0)
            self.Control.m1.value(0)
            self.Control.m2.value(1)
        elif steps == 5:
            self.Control.m0.value(1)
            self.Control.m1.value(1)
            self.Control.m2.value(1)

    def addparametrs(self):
        self.Control.rotation_callback = self.__callback
        self.Control.rotation_set = self.__set
        self.Control.redata['!pwm_f'] = 1
        self.Control.redata['!rotation_reverse'] = False
        self.Control.redata['!steps'] = 0
        
        self.Control.readfile(self.Control.profile_folder+'/rotation/','default.conf', self.__read)
        
        self.Control.dir.value(self.Control.redata['!rotation_reverse'])
        self.Control.pwm.freq(self.Control.redata['!pwm_f'])
        self.setdivider(self.Control.redata['!steps'])  

    def __read(self, name, read):
        if  name == 'frequency':
            self.Control.redata['!pwm_f'] = int(read)
        elif name == 'reverse':
            self.Control.redata['!rotation_reverse'] = read == 'True'
        elif name == 'steps':
            self.Control.redata['!steps'] = int(read)

    def removeparametrs(self):
        self.Control.rotation_callback = None
        self.Control.rotation_set = None
        self.Control.redata.pop('!pwm_f', None)
        self.Control.redata.pop('!rotation_reverse', None)
        self.Control.redata.pop('!steps', None)

    def stop(self):
        self.isenable = False
        self.Control.rst.value(0)
        self.Control.pwm.duty(0)

def create(p):
    return default(p)
