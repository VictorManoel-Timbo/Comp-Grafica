import pygame 
from pygame.locals import *
import sys
from primitive import Primitive
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1024, 768
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.drawer = Primitive(self._display_surf)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        if self.drawer:
            self.drawer.draw_line_bress(150, 200, 200, 250)
            self.drawer.draw_circunference_bress(200, 150, 50, (255, 255, 255))
            self.drawer.draw_elipse(200, 150, 90, 60, (255, 255, 255))
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit()
        sys.exit()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        pygame.display.set_caption("Set Pixel")

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()