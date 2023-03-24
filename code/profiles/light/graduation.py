#load:Graduation:
from uasyncio import sleep_ms
class onecolor:
    def __init__(self, control):
        self.confpath = control.profile_folder+'/light/graduation.conf'
        self.Control = control
        self.isenable = False
        self.ccolor = 0
        self.startcolor = ()
        self.stopcolor = ()
        self.mocolor = True

    async def start(self):
        self.isenable = True
        self.ccolor = 0
        self.startcolor = ()
        self.stopcolor = ()
        self.mocolor = True
        while self.isenable:
            getcolors = self.Control.redata['!hc'].replace('#','').split(',')
            if '' in getcolors:
                getcolors.remove('')
            if len(getcolors) == 0:
                self.Control.np.fill((0,0,0))
                self.Control.np.write()
                self.mocolor = True
            elif len(getcolors) == 1:
                if self.startcolor == ():
                    self.startcolor = self.hex_to_rgb(getcolors[0])
                    self.Control.np.fill(self.startcolor)
                    self.Control.np.write()
                    self.mocolor = True
            elif len(getcolors) > 1:
                if self.startcolor == () and self.mocolor:
                    self.mocolor = False
                    self.startcolor = self.hex_to_rgb(getcolors[self.ccolor])
                    self.ccolor +=1
                    continue
                self.Control.np.fill(self.startcolor)
                self.Control.np.write()

                self.stopcolor = self.hex_to_rgb(getcolors[self.ccolor])

                sta_r = self.startcolor[0]
                sta_g = self.startcolor[1]
                sta_b = self.startcolor[2]
                step_r = (sta_r-self.stopcolor[0])/255*-1
                step_g = (sta_g-self.stopcolor[1])/255*-1
                step_b = (sta_b-self.stopcolor[2])/255*-1

                for step in range(255):
                    if not self.isenable: break;
                    sta_r += step_r
                    sta_g += step_g
                    sta_b += step_b
                    self.Control.np.fill((int(sta_r),int(sta_g),int(sta_b)))
                    self.Control.np.write()
                    await sleep_ms(int(self.Control.redata['!delay_change']))

                self.startcolor = self.stopcolor
                self.ccolor += 1
                if self.ccolor > len(getcolors)-1:
                    self.ccolor = 0
            await sleep_ms(int(self.Control.redata['!delay_change']))

    def hex_to_rgb(self, hexa):
        return tuple(int(hexa[i:i+2], 16)  for i in (0, 2, 4))

    def __light_set(self, type_data, data):
        if type_data == 'updatecolor':
            splitdata = data.split('\\')
            self.Control.redata['!hc'] = splitdata[0]
            self.Control.redata['!id_button_colors'] = splitdata[1]
        elif type_data == 'setdelay':
            self.Control.redata['!delay_change'] = data
        self.Control.writefile(self.confpath,
        'colors:'+self.Control.redata['!hc']+'\n'+
        'id_buttons:'+self.Control.redata['!id_button_colors']+'\n'+
        'delay_change:'+str(self.Control.redata['!delay_change'])+'\n')

    async def __callback(self, request):
        await self.Control.sendfile(request, '/profiles/light/','graduation.web')

    def addparametrs(self):
        self.Control.light_callback = self.__callback
        self.Control.light_set = self.__light_set
        self.Control.redata['!hc'] = ''
        self.Control.redata['!id_button_colors'] = ''
        self.Control.redata['!delay_change'] = '10'
        self.Control.readfile(self.Control.profile_folder+'/light/','graduation.conf', self.__read)

    def __read(self, name, read):
        if  name == 'colors':
            self.Control.redata['!hc'] = read
        elif name == 'delay_change':
            self.Control.redata['!delay_change'] = int(read)
        elif name == 'id_buttons':
            self.Control.redata['!id_button_colors'] = read

    def removeparametrs(self):
        self.Control.light_callback = None
        self.Control.light_set = None
        self.Control.redata.pop('!hc', None)
        self.Control.redata.pop('!id_button_colors', None)
        self.Control.redata.pop('!delay_change', None)

    def stop(self):
        self.isenable = False
        self.ccolor = 0
        self.startcolor = ()
        self.stopcolor = ()
        self.Control.np.fill((0, 0, 0))
        self.Control.np.write()
        self.mocolor = True

def create(p):
    return onecolor(p)
