#load:Random:
from uasyncio import sleep_ms
import urandom

class onecolor:
    def __init__(self, control):
        self.Control = control
        self.isenable = False

    async def start(self):
        self.isenable = True
        leds = len(self.Control.np)
        while self.isenable:
            color = [self.randint(1,254),self.randint(1,254),self.randint(1,254)]
            r = self.randint(1,leds)
            for l in range(r-1):
                led = self.randint(1,leds)
                self.Control.np[led-1] = color
            self.Control.np.write()
            await sleep_ms(150)

    def randint(self, min, max):
        span = max - min + 1
        div = 0x3fffffff // span
        offset = urandom.getrandbits(30) // div
        val = min + offset
        return val

    def __light_set(self, type_data, data):
        pass

    async def __callback(self, request):
        await self.Control.sendfile(request, '/profiles/light/','random.web')

    def addparametrs(self):
        self.Control.light_callback = self.__callback
        self.Control.light_set = self.__light_set
        pass

    def removeparametrs(self):
        pass

    def stop(self):
        self.isenable = False
        self.Control.np.fill((0, 0, 0))
        self.Control.np.write()

def create(p):
    return onecolor(p)
