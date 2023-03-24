#load:One color:
from uasyncio import sleep_ms
import os

class onecolor:
    def __init__(self, control):
        self.confpath = control.profile_folder+'/light/one_color.conf'
        self.Control = control
        self.isenable = False
        self.color = [127,127,127]
        self.oldcolor = [0, 0, 0]

    async def start(self):
        self.isenable = True
        while self.isenable:
            if not self.color == self.oldcolor:
                self.oldcolor = self.color
                self.Control.np.fill(self.color)
                self.Control.np.write()
            await sleep_ms(10)

    def __light_set(self, type_data, data):
        if type_data == 'monocolor':
            splitdata = data.split(',')
            self.color = [int(splitdata[0]),int(splitdata[1]),int(splitdata[2])]
            self.Control.redata['!r_c'] = self.color[0]
            self.Control.redata['!g_c'] = self.color[1]
            self.Control.redata['!b_c'] = self.color[2]
            self.Control.writefile(self.confpath,
                                   'r_c:'+str(self.Control.redata['!r_c'])+'\n'+
                                   'g_c:'+str(self.Control.redata['!g_c'])+'\n'+
                                   'b_c:'+str(self.Control.redata['!b_c'])+'\n')

    async def __callback(self, request):
        await self.Control.sendfile(request, '/profiles/light/','onecolor.web')

    def addparametrs(self):
        self.Control.light_callback = self.__callback
        self.Control.light_set = self.__light_set
        self.Control.redata['!r_c'] = self.color[0]
        self.Control.redata['!g_c'] = self.color[1]
        self.Control.redata['!b_c'] = self.color[2]

        if not 'one_color.conf' in os.listdir(self.Control.profile_folder+'/light/'):
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
        file.close()
        self.color = [self.Control.redata['!r_c'],self.Control.redata['!g_c'],self.Control.redata['!b_c']]

    def removeparametrs(self):
        self.Control.light_callback = None
        self.Control.light_set = None
        self.Control.redata.pop('!r_c', None)
        self.Control.redata.pop('!g_c', None)
        self.Control.redata.pop('!b_c', None)

    def stop(self):
        self.isenable = False
        self.oldcolor = [0, 0, 0]
        self.Control.np.fill((0, 0, 0))
        self.Control.np.write()

def create(p):
    return onecolor(p)
