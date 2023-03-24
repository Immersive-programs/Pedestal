#load:Manual:
from uasyncio import sleep_ms
import os

class manual:
    def __init__(self, control):
        self.confpath = control.profile_folder+'/light/manual.conf'
        self.Control = control
        self.isenable = False
        self.ledpos = []
        self.color = [127,127,127]
        self.oldcolor = [0, 0, 0]

    async def start(self):
        self.isenable = True
        while self.isenable:
            if not self.color == self.oldcolor:
                self.oldcolor = self.color

                for pos in self.ledpos:
                    try:
                        self.Control.np[pos] = self.color
                        
                    except:pass
                    
                saveleds = ''    
                for pos in range(self.Control.redata['!np_leds']-1):
                    scolor = self.Control.np[pos]
                    saveleds += str(pos)+':'+str(scolor[0])+','+str(scolor[1])+','+str(scolor[2])+'\n'
                self.Control.writefile(self.confpath, saveleds)
                self.Control.np.write()
            await sleep_ms(10)

    def __light_set(self, type_data, data):
        if type_data == 'monocolor':
            splitdata = data.split(',')
            self.color = [int(splitdata[0]),int(splitdata[1]),int(splitdata[2])]
            self.Control.redata['!r_c'] = self.color[0]
            self.Control.redata['!g_c'] = self.color[1]
            self.Control.redata['!b_c'] = self.color[2]
        elif type_data == 'setleds':
            try:
                if '-' in data:
                    splitdata = data.split('-')
                    self.ledpos = []
                    for u in range(int(splitdata[0]),int(splitdata[1])+1):
                        self.ledpos.append(u)
                else:
                    self.ledpos = [int(data),]
            except:pass

    async def __callback(self, request):
        await self.Control.sendfile(request, '/profiles/light/','manual.web')

    def addparametrs(self):
        self.Control.light_callback = self.__callback
        self.Control.light_set = self.__light_set
        self.Control.redata['!r_c'] = self.color[0]
        self.Control.redata['!g_c'] = self.color[1]
        self.Control.redata['!b_c'] = self.color[2]
        self.Control.redata['!np_leds'] = len(self.Control.np)

        if not 'manual.conf' in os.listdir(self.Control.profile_folder+'/light/'):
            open(self.confpath,'x').close()
        file = open(self.confpath)
        while True:
            line = file.readline()
            if not line:
                break
            read = line.split(':')
            if len(read) > 1:
                splitcolor = read[1].split(',')
                try:
                    self.Control.np[int(read[0])] = (int(splitcolor[0]),int(splitcolor[1]),int(splitcolor[2]))
                except:pass
        file.close()
        self.Control.np.write()

    def removeparametrs(self):
        self.Control.light_callback = None
        self.Control.light_set = None
        self.Control.redata.pop('!r_c', None)
        self.Control.redata.pop('!g_c', None)
        self.Control.redata.pop('!b_c', None)

    def stop(self):
        self.isenable = False
        self.oldcolor = [0, 0, 0]
        self.ledpos = []
        self.Control.np.fill((0, 0, 0))
        self.Control.np.write()

def create(p):
    return manual(p)
