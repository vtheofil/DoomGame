from settings import * 
import pygame as pg 
import math


class Player:
        def __init__(self,game):
            self.game = game  # Αναφορά στο αντικείμενο του παιχνιδιού
            self.x, self.y = PLAYER_POS  # Αρχική θέση του παίκτη
            self.angle = PLAYER_ANGLE  # Αρχική γωνία (κατεύθυνση στην οποία κοιτάει ο παίκτης)
            self.shot = False  # Boolean για να παρακολουθήσουμε αν ο παίκτης έχει πυροβολήσει
            self.health = PLAYER_MAX_HEALTH  # Ορίζουμε την υγεία του παίκτη στο μέγιστο
            self.rel = 0  # Σχετική κίνηση του ποντικιού για περιστροφή
            self.health_recovery_delay = 700  # Καθυστέρηση για την αποκατάσταση υγείας (σε χιλιοστά του δευτερολέπτου)
            self.time_prev = pg.time.get_ticks()  # Χρονική στιγμή στην οποία ξεκινάει το παιχνίδι (σε χιλιοστά του δευτερολέπτου)
     
        def recover_health(self): # Μέθοδος για την αποκατάσταση υγείας με την πάροδο του χρόνου
            if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
                self.health +=1 # Αυξάνει την υγεία κατά 1 αν επιτρέπεται η αποκατάσταση
        
        # Έλεγχος αν έχει περάσει αρκετός χρόνος για να επιτραπεί η αποκατάσταση υγείας
        def check_health_recovery_delay(self):
            time_now = pg.time.get_ticks()  # Παίρνουμε την τρέχουσα χρονική στιγμή (σε χιλιοστά του δευτερολέπτου)
            if time_now - self.time_prev > self.health_recovery_delay: 
                self.time_prev = time_now  # Ενημερώνουμε το χρόνο
                return True # Επιστρέφουμε True για να επιτρέψουμε την αποκατάσταση υγείας
            
        def check_game_over(self):
            if self.health < 1:
                self.game.object_renderer.game_over() # Καλούμε τη μέθοδο game over
                pg.display.flip() # Ενημερώνουμε την οθόνη
                pg.time.delay(1500)  # Περιμένουμε 1,5 δευτερόλεπτα πριν το επόμενο παιχνίδι
                self.game.new_game() # Ξεκινάμε ένα νέο παιχνίδι
            
            # Μέθοδος για να πάρει ζημιά ο παίκτης
        def get_damage(self, damage):  
            self.health -= damage  # Μειώνουμε την υγεία του παίκτη
            self.game.object_renderer.player_damage()  # Καλούμε την αναπαράσταση του τραυματισμένου παίκτη
            self.game.sound.player_pain.play()  # Παίζουμε ήχο πόνου του παίκτ
            self.check_game_over() # Ελέγχουμε αν η υγεία έχει φτάσει στο 0
            
            # Μέθοδος για τον χειρισμό του πυροβολισμού
        def single_fire_event(self, event):
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot and not self.game.weapon.reloading: # Αριστερό κλικ και δεν έχει ξαναπυροβολήσει
                    self.game.sound.shotgun.play()  # Παίζουμε τον ήχο του πυροβολισμού
                    self.shot = True  # Σημειώνουμε ότι ο παίκτης έχει πυροβολήσει
                    self.game.weapon.reloading = True # Ενεργοποιούμε το αναγκαίο reload όπλου
            
            # Μέθοδος για την κίνηση του παίκτη
        def movement(self):
            sin_a = math.sin(self.angle)   # Υπολογισμός του ημίτονου της γωνίας
            cos_a = math.cos(self.angle) # Υπολογισμός του συνημίτονου της γωνίας
            dx, dy = 0, 0  # Αρχικοί ρυθμοί κίνησης στον άξονα x και y
            speed = PLAYER_SPEED * self.game.delta_time # Ταχύτητα με βάση τον χρόνο ανανέωσης
            speed_sin = speed * sin_a  # Κίνηση στον άξονα y
            speed_cos = speed * cos_a # Κίνηση στον άξονα x
            
            keys = pg.key.get_pressed() # Λήψη των πατημένων πλήκτρων
            if keys [pg.K_w]: # Αν πατηθεί το W
                dx += speed_cos  # Κίνηση μπροστά στον άξονα x
                dy += speed_sin # Κίνηση μπροστά στον άξονα y
            if keys[pg.K_s]: # Αν πατηθεί το S
                dx += -speed_cos  # Κίνηση πίσω στον άξονα x
                dy += -speed_sin  # Κίνηση πίσω στον άξονα y
            if keys[pg.K_a]:  # Αν πατηθεί το A
                dx += speed_sin # Κίνηση αριστερά στον άξονα x
                dy += -speed_cos  # Κίνηση αριστερά στον άξονα y
            if keys[pg.K_d]: # Αν πατηθεί το D
                dx += -speed_sin    # Κίνηση δεξιά στον άξονα x
                dy += speed_cos   # Κίνηση δεξιά στον άξονα y
                
            self.check_wall_collision(dx, dy)  # Έλεγχος για σύγκρουση με τοίχο
            
            
        #    if keys[pg.K_LEFT]:
         #        self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
          #  if keys[pg.K_RIGHT]:
           #      self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        
            # Περιστροφή με το ποντίκι
            
            self.angle %= math.tau  # Κρατάει τη γωνία εντός [0, 2π]
            # Μέθοδος για να ελέγξει αν υπάρχει τοίχος στη θέση που κινείται ο παίκτης 
        def check_wall(self,x,y):
            return(x,y) not in self.game.map.world_map # Αν η θέση δεν είναι στον χάρτη, επιστρέφει False
        
        # Μέθοδος για να ελέγξει αν υπάρχει σύγκρουση με τοίχο
        def check_wall_collision(self,dx,dy): 
            scale = PLAYER_SIZE_SCALE / self.game.delta_time # Κλίμακα κίνησης
            if self.check_wall(int(self.x + dx * scale), int(self.y)):  # Έλεγχος σύγκρουσης στον άξονα x
                self.x += dx   # Αν δεν υπάρχει σύγκρουση, μετακινούμε τον παίκτη
            if self.check_wall(int(self.x), int(self.y +dy * scale)):  # Έλεγχος σύγκρουσης στον άξονα y
                self.y += dy  # Αν δεν υπάρχει σύγκρουση, μετακινούμε τον παίκτη
         
            # Μέθοδος για να σχεδιάσει τον παίκτη στην οθόνη
        def draw(self):
           # pg.draw.line(self.game.screen, 'yellow', (self.x * 100 , self.y * 100),
           #              (self.x * 100 + WIDTH *math.cos(self.angle),
           #                self.y * 100 + WIDTH * math.sin(self.angle)),2)
            pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y*100),15)   # Σχεδιάζει έναν κύκλο για τον παίκτη
        
        # Μέθοδος για να ελέγξει τον έλεγχο με το ποντίκι
        def mouse_control(self):
            mx, my = pg.mouse.get_pos()  # Παίρνουμε τη θέση του ποντικιού
            if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:  # Αν το ποντίκι βγει από τα όρια
                pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])  # Επαναφέρουμε το ποντίκι στο κέντρο
            self.rel = pg.mouse.get_rel()[0] # Υπολογίζουμε την κίνηση του ποντικιού
            self.rel = max (-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))  # Περιορίζουμε τη σχετική κίνηση
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time  # Ενημερώνουμε την γωνία με βάση την κίνηση του ποντικιού
           
            # Μέθοδος για την ενημέρωση του παίκτη κάθε καρέ
        def update(self): 
            self.movement() # Ενημερώνουμε την κίνηση του παίκτη
            self.mouse_control()  # Ελέγχουμε την περιστροφή με το ποντίκι
            self.recover_health()  # Προσπαθούμε να ανακτήσουμε υγεία
          
            # Προσπαθούμε να ανακτήσουμε υγεία
        @property
        def pos(self):
            return self.x,self.y
        # Ιδιότητα για να επιστρέψουμε τη θέση του παίκτη στον χάρτη (όπως είναι στο grid)
        @property
        def map_pos(self):
            return int(self.x), int(self.y)
        


