from machine import Pin, PWM
from neopixel import NeoPixel
from nanoweb import Nanoweb
from utime import sleep_ms
import uasyncio
import network
import os
import gc

RGB_Leds = 24
RGB_Pin = 27

M0 = 17
M1 = 5
M2 = 16
STEP = 12
RST = 25
DIR = 26

class Main:
    def __init__(self):
        self.np = NeoPixel(Pin(RGB_Pin), RGB_Leds)
        self.np.fill((0, 0, 0))
        self.np.write()

        self.pwm = PWM(Pin(STEP))
        self.pwm.freq(1)
        self.pwm.duty(0)

        self.m0 = Pin(M0,Pin.OUT)
        self.m1 = Pin(M1,Pin.OUT)
        self.m2 = Pin(M2,Pin.OUT)
        self.dir = Pin(DIR,Pin.OUT)

        self.m0.value(0)
        self.m1.value(0)
        self.m2.value(0)
        self.dir.value(0)

        self.rst = Pin(RST,Pin.OUT)
        self.rst.value(0)

        self.redata = {
            '!light_status': False,
            '!light_index': -1,
            '!light_mode': 'One color',
            '!light_profiles':'',
            '!rotation_status': False,
            '!rotation_index': -1,
            '!rotation_mode': 'Default',
            '!rotation_profiles':'',
            }

        self.langs ={
            'ru' : 'Русский',
            'en' : 'English',
            }
        
        self.lang = 'en'

        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.active(False)

        self.profile_name = 'default'
        self.profile_folder = '/profiles/user/'+self.profile_name
        self.try_mkdir(self.profile_folder)
        
        self.autostart_light = False
        self.autostart_rotation = False
        self.autoconnet = True

        self.useap = False

        self.device_name = 'Pedestal'
        self.ap_pass = '9876543210'
        self.wlan_id = ''
        self.wlan_pass = ''

        if not 'settings.conf' in os.listdir('/'):
            open('settings.conf','x').close()
        settings = open('settings.conf')
        while True:
            line = settings.readline()
            if not line:
                break
            read = line.split(':')
            if len(read) > 1:
                if  read[0] == 'a_l':
                    self.autostart_light = read[1] == 'True\n'
                elif read[0] == 'a_r':
                    self.autostart_rotation = read[1] == 'True\n'
                elif read[0] == 'ac':
                    self.autoconnet = read[1] == 'True\n'
                elif read[0] == 'w_id':
                    self.wlan_id = read[1][:-1]
                elif read[0] == 'w_p':
                    self.wlan_pass = read[1][:-1]
                elif read[0] == 'ap':
                    self.ap_pass = read[1][:-1]
                elif read[0] == 'd':
                    self.device_name = read[1][:-1]
                elif read[0] == 'l':
                    self.redata['!light_mode'] = read[1][:-1]
                elif read[0] == 'r':
                    self.redata['!rotation_mode'] = read[1][:-1]
                elif read[0] == 'lang':
                     self.lang = read[1][:-1]
                
        settings.close()

        if self.wlan_id == '' or self.wlan_pass == '':
            self.start_ap()

        if self.autostart_light:
            self.redata['!light_status'] = True
        if self.autostart_rotation:
            self.redata['!rotation_status'] = True

        if not self.useap and self.autoconnet:
            time = 5000
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.disconnect()
            sleep_ms(1)
            self.wlan.config(dhcp_hostname = self.device_name)
            self.wlan.connect(self.wlan_id, self.wlan_pass)
            while self.wlan.ifconfig()[0] == '0.0.0.0' and time > 0:
                time -= 1
                sleep_ms(1)

        if self.wlan.ifconfig()[0] == '0.0.0.0' and not self.useap or not self.autoconnet:
            self.wlan.active(False)
            self.start_ap()

        self.naw = Nanoweb()
        self.naw.STATIC_DIR = '/source/'
        self.naw.routes = {
            '/settings': self.globalsettings,
            '/settings/light': self.lightsettings,
            '/settings/rotation': self.rotationsettings,
            '/data': self.data,
            '/': self.root}
        self.naw.extract_headers = self.naw.extract_headers + ('New_Data',)

        self.light_profile_selected = None
        self.light_set = None
        self.light_callback = None
        self.light_profiles = self.searchprofiles('/profiles/light/')

        self.rotation_profile_selected = None
        self.rotation_set = None
        self.rotation_callback = None
        self.rotation_profiles = self.searchprofiles('/profiles/rotation/', False)

        if self.redata['!light_mode'] in self.light_profiles['names']:
            index = self.light_profiles['names'].index(self.redata['!light_mode'])
            self.redata['!light_index'] = index
            self.light_profile_selected = __import__(self.light_profiles['profiles'][index]).create(self)
        gc.collect()

        if self.redata['!rotation_mode'] in self.rotation_profiles['names']:
            index = self.rotation_profiles['names'].index(self.redata['!rotation_mode'])
            self.redata['!rotation_index'] = index
            self.rotation_profile_selected = __import__(self.rotation_profiles['profiles'][index]).create(self)
        gc.collect()

        if not self.redata['!light_index'] == -1:
            self.light_profile_selected.addparametrs()
        if not self.redata['!rotation_index'] == -1:
            self.rotation_profile_selected.addparametrs()

        self.loop = uasyncio.get_event_loop()
        self.loop.create_task(self.naw.run())

        if self.redata['!light_status']:
            self.loop.create_task(self.light_profile_selected.start())
        if self.redata['!rotation_status']:
            self.loop.create_task(self.rotation_profile_selected.start())
        gc.collect()
        self.loop.run_forever()

    def start_ap(self):
        self.useap = True
        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.active(True)
        self.wlan.config(essid = self.device_name, password = self.ap_pass)

    def data(self, request):
        await request.write("HTTP/1.1 200 OK\r\n\r\n")
        newdata = request.headers.get('New_Data', None)
        if newdata == None:
            await request.write('Data Only')
            return

        splitdata = newdata.split('|')
        if '' in splitdata:
            splitdata.remove('')
        for data in splitdata:
            get = data.split(':')
            if get[0] == 'light_status':
                self.redata['!light_status'] = get[1] == 'true'
                if self.redata['!light_status']:
                    self.loop.create_task(self.light_profile_selected.start())
                else:
                    self.light_profile_selected.stop()
            elif get[0] == 'rotation_status':
                self.redata['!rotation_status'] = get[1] == 'true'
                if self.redata['!rotation_status']:
                    self.loop.create_task(self.rotation_profile_selected.start())
                else:
                    self.rotation_profile_selected.stop()
            elif get[0] == 'light_mode':
                if get[1] == '-1':
                    return
                mode = int(get[1])
                if not mode == self.redata['!light_index']:
                    self.redata['!light_index'] = mode
                    self.redata['!light_mode'] = self.light_profiles['names'][mode]
                    self.light_profile_selected.stop()
                    self.light_profile_selected.removeparametrs()
                    gc.collect()
                    self.light_profile_selected = __import__(self.light_profiles['profiles'][mode]).create(self)
                    self.light_profile_selected.addparametrs()
                    self.savesettings()
                    if self.redata['!light_status']:
                        self.loop.create_task(self.light_profile_selected.start())
                await self.light_callback(request)
            elif get[0] == 'rotation_mode':
                if get[1] == '-1':
                    return
                mode = int(get[1])
                if not mode == self.redata['!rotation_index']:
                    self.redata['!rotation_index'] = mode
                    self.redata['!light_mode'] = rotation_names_profiles[mode]
                    self.rotation_profile_selected.stop()
                    self.rotation_profile_selected.removeparametrs()
                    gc.collect()
                    self.rotation_profile_selected = __import__(self.rotation_profiles[mode]).create(self)
                    self.rotation_profile_selected.addparametrs()
                    self.savesettings()
                    if self.redata['!rotation_status']:
                        self.loop.create_task(self.rotation_profile_selected.start())
                await self.rotation_callback(request)
            elif get[0] == 'light_set':
                self.light_set(get[1],get[2])
            elif get[0] == 'rotation_set':
                self.rotation_set(get[1],get[2])
            elif get[0] == 'getsystemsettings':
                lsend = ''
                for l in self.langs:lsend += l +'*'+ self.langs[l]+'\\'
                
                await request.write(str(self.autostart_light)+','+
                                    str(self.autostart_rotation)+','+
                                    self.device_name+','+
                                    self.wlan_id+','+
                                    self.wlan_pass+','+
                                    self.ap_pass+','+
                                    str(self.autoconnet)+','+
                                    self.lang+','+
                                    lsend)
            elif get[0] == 'setsystemsettings':
                splitsettings = get[1].split(',')
                self.autostart_light = splitsettings[0] == 'true'
                self.autostart_rotation = splitsettings[1] == 'true'
                self.autoconnet = splitsettings[2] == 'true'
                self.wlan_id = splitsettings[3]
                self.wlan_pass = splitsettings[4]
                self.ap_pass = splitsettings[5]
                self.device_name = splitsettings[6]
                self.lang = splitsettings[7]
                self.savesettings()
        gc.collect()

    def root(self, request):
        await request.write("HTTP/1.1 200 OK\r\n\r\n")
        path = '/source/html/indexes/'
        await self.sendfile(request, path, self.lang + '.html')

    def globalsettings(self, request):
        await request.write("HTTP/1.1 200 OK\r\n\r\n")
        path = '/source/html/settings/'
        await self.sendfile(request, path, self.lang + '.html')

    def lightsettings(self, request):
        await request.write("HTTP/1.1 200 OK\r\n\r\n")
        path = '/source/html/settings/light/'
        await self.sendfile(request, path, self.lang + '.html')

    def rotationsettings(self, request):
        await request.write("HTTP/1.1 200 OK\r\n\r\n")
        path = '/source/html/settings/rotation/'
        await self.sendfile(request, path, self.lang + '.html')

    def replace_data(self,data):
        for re in self.redata:
            if re in data:
                data = data.replace(re,str(self.redata[re]))
        return data

    async def sendfile(self, request, path, name):
        if not name in os.listdir(path):
            return ''
        fpath = path + name
        page = open(fpath)
        buff = ''
        while True:
            line = page.readline()
            if not line:
                break
            await request.write(self.replace_data(line))
        gc.collect()

    def writefile(self, path, write):
        file = open(path,'w')
        file.write(write)
        file.close()

    def readfile(self, path, name, callback):
        self.try_mkdir(path)
        if not name in os.listdir(path):
            open(path+name,'x').close()
        settings = open(path+name)
        while True:
            line = settings.readline()
            if not line:
                break
            read = line.split(':')
            callback(read[0],read[1][:-1])
            
    def savesettings(self):
        self.writefile('settings.conf',
               'a_l:'+str(self.autostart_light)+'\n'+
               'a_r:'+str(self.autostart_rotation)+'\n'+
               'ac:'+str(self.autoconnet)+'\n'+
               'w_id:'+self.wlan_id+'\n'+
               'w_p:'+self.wlan_pass+'\n'+
               'ap:'+self.ap_pass+'\n'+
               'd:'+self.device_name+'\n'+
               'l:'+self.redata['!light_mode']+'\n'+
               'r:'+self.redata['!rotation_mode']+'\n'+
               'lang:'+self.lang+'\n')
            
    def try_mkdir(self, path):
            splitpath = path.split('/')
            fpath = ''
            for d in splitpath:
                if d == '':
                    continue
                fpath += d
                try:
                    os.mkdir('/'+fpath)
                except:pass
                fpath+='/'

    def searchprofiles(self, path, re = True):
        back = {
            'profiles': [],
            'names':  [],
        }
        glist = os.listdir(path)
        for file in glist:
            fill = path + file
            f = open(fill)
            first_line = f.readline()
            f.close()
            if 'load:' in first_line:
                sl = first_line.split(':')
                back['names'].append(sl[1])
                back['profiles'].append(fill.replace('.py',''))
                if re:
                    self.redata['!light_profiles'] += sl[1]+','
                else:
                    self.redata['!rotation_profiles'] += sl[1]+','
        return back;

Main()
