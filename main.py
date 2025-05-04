import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import*
from sprite_object import*
from object_handler import*
from weapon import*
from sound import*
from pathfinding import*

class Game :    # Κύρια κλάση του παιχνιδιού 
    def __init__(self):
        pg.init() 
        pg.mouse.set_visible(False) # Απόκρυψη του ποντικιού κατά τη διάρκεια του παιχνιδιού
        self.screen = pg.display.set_mode(res)
        self.clock = pg.time.Clock() # Ρολόι για τον έλεγχο του χρόνου (π.χ., FPS)
        self.delta_time= 1  # Αρχικοποίηση της μεταβλητής για το χρονικό διάστημα μεταξύ καρέ
        self.global_trigger = False  #  μεταβλητή ενεργοποίησης για γεγονότα
        self.global_event = pg.USEREVENT + 0   # Ορισμός ενός προσαρμοσμένου γεγονότος για χρονόμετρα
        pg.time.set_timer(self.global_event, 40 ) # Ενεργοποίηση του κάθε 40ms
         
        self.new_game()
        
    def new_game(self):
        self.map = Map(self) # Δημιουργία αντικειμένου χάρτη
        self.player = Player(self) # Δημιουργία αντικειμένου παίκτη
        self.object_renderer = ObjectRendere(self)     # Renderer για την απόδοση των αντικειμένων στην οθόνη
        self.raycasting = RayCasting(self)         # Δημιουργία αντικειμένου raycasting για τον υπολογισμό της ορατότητας
        self.object_handler = ObjectHandler(self)  # Χειριστής αντικειμένων (π.χ., NPCs ή άλλα δυναμικά αντικείμενα)
        self.weapon = Weapon(self)         # Δημιουργία του όπλου του παίκτη
        self.sound = Sound(self)           # Φόρτωση και διαχείριση ήχων
        self.pathfinding = PathFinding(self)          # Αλγόριθμος εύρεσης διαδρομής (Pathfinding)
        pg.mixer.music.play(-1)
    
    def update(self):
        # Ενημέρωση όλων των συστημάτων του παιχνιδιού σε κάθε καρέ
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS) # Υπολογισμός του χρονικού διαστήματος μεταξύ καρέ
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
       # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
       # self.map.draw()
        #self.player.draw()
        
        
    def check_events(self): # Έλεγχος για γεγονότα (π.χ., πάτημα πλήκτρων, έξοδος παιχνιδιού)
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit() 
            elif event.type == self.global_event:
                self.global_trigger = True 
            self.player.single_fire_event(event)
        
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            
            
if __name__ == '__main__':
    game = Game()
    game.run()            
            

