import pygame as pg 
from settings import * 
import os
from collections import deque

class SpriteObject:
    def __init__(self, game , path = r"AssetsGame\sprites\static_sprites\candlebra.png", pos=(10.5,3.5), scale= 0.7,shift=0.27):
        self.game = game 
        self.player = game.player  # Αναφορά στον παίκτη για σχετική τοποθέτηση.
        self.x, self.y = pos  # Θέση του sprite στον κόσμο του παιχνιδιού.
        self.image = pg.image.load(path).convert_alpha() # Φορτώνει την εικόνα του sprite.
        self.IMAGE_WIDTH = self.image.get_width() # Πλάτος της εικόνας.
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2  # Μισό πλάτος της εικόνας.
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height() # Αναλογία πλάτους-ύψους της εικόνας
        self.dx, self.dy, self.theta, self.screen_x,self.dist, self.norm_dist = 0,0,0,0,1,1
        self.sprite_half_width = 0  # Μισό πλάτος του sprite που θα χρησιμοποιηθεί στην προβολή
        self.SPRITE_SCALE = scale # Κλίμακα του sprite
        self.SPRITE_HEIGHT_SHIFT = shift  # Μετατόπιση για το ύψος του sprite
        
        
    def get_sprite_projection(self):
        """
       Υπολογίζει την προβολή του sprite στην οθόνη με βάση τη θέση του στον κόσμο και τη θέση του παίκτη.
       """
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE # Υπολογισμός προβολής
        proj_width , proj_height = proj * self.IMAGE_RATIO, proj # Υπολογισμός πλάτους και ύψους προβολής
        
        image = pg.transform.scale(self.image, (proj_width, proj_height)) # Αλλαγή μεγέθους της εικόνας σύμφωνα με την προβολή.
        
        self.sprite_half_width = proj_width // 2 # Υπολογισμός της θέσης του sprite στην οθόνη.
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self . screen_x - self.sprite_half_width , HALF_HEIGHT - proj_height // 2 + height_shift
        
        self.game.raycasting.objects_to_render.append((self.norm_dist,image,pos))  # Προσθήκη του sprite στη λίστα με τα αντικείμενα προς απόδοση
        
    def get_sprite(self):
        """
      Υπολογίζει τη θέση του sprite σε σχέση με τον παίκτη και αν είναι ορατό στην οθόνη.
      """
        dx = self.x - self.player.x  # Απόσταση του sprite από τον παίκτη στον άξονα x
        dy = self.y - self.player.y  # Απόσταση του sprite από τον παίκτη στον άξονα y.
        self.dx , self.dy = dx, dy 
        self.theta = math.atan2(dy,dx)   # Γωνία του sprite σε σχέση με τον παίκτη
        
        # Υπολογισμός της γωνίας ανάμεσα στο sprite και την κατεύθυνση του παίκτη.
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0 ):
            delta += math.tau
        
        # Μετατροπή της γωνίας σε ακτίνες για την οθόνη.
        delta_rays = delta / DELTA_ANGLE 
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE 
        
        # Υπολογισμός απόστασης και κανονικοποίησής της.
        self.dist = math.hypot(dx,dy) # Απόσταση μεταξύ sprite και παίκτη
        self.norm_dist = self.dist * math.cos(delta) # Κανονικοποιημένη απόσταση
        # Αν το sprite είναι ορατό στην οθόνη και αρκετά κοντά, γίνεται προβολή.
        if -self.IMAGE_HALF_WIDTH <self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5 :
            self.get_sprite_projection()
    
    def update(self):
        self.get_sprite()
        """
        Ενημερώνει την κατάσταση του sprite σε κάθε frame.
        """
        
        
class AnimatedSprite(SpriteObject):
    """
   Αντιπροσωπεύει ένα κινούμενο sprite.
   """
    def __init__(self, game , path=r"AssetsGame\animatedSprites\0.png", pos = (11.5, 3.5), scale = 0.8, shift=0.15,animation_time=120):
        super().__init__(game,path,pos,scale,shift)
        self.animation_time = animation_time
        self.path = os.path.dirname(path)  # Διαδρομή του φακέλου με τις εικόνες της κίνησης
        self.images = self.get_images(self.path) # Φορτώνει όλες τις εικόνες για την κίνηση
        
        if self.images:  # Αν υπάρχουν εικόνες, ορίζουμε την πρώτη
            self.image = self.images[0]
        self.animation_time_prev = pg.time.get_ticks()  # Χρόνος τελευταίας αλλαγής καρέ
        self.animation_trigger = False
        
    def update(self):
        """
       Ενημερώνει την κατάσταση του κινούμενου sprite.
       """
        super().update()
        self.check_animation_time()  # Ελέγχει αν είναι ώρα για αλλαγή καρέ
        self.animate(self.images) # Ενημερώνει την τρέχουσα εικόνα της κίνησης
        
    def animate(self, images):
        """
        Αλλάζει την τρέχουσα εικόνα της κίνησης.
        """
        if self.animation_trigger:
            images.rotate(-1) # Περιστροφή της λίστας εικόνων.
            self.image = images[0]  # Επιλογή της επόμενης εικόνας
        
    def check_animation_time(self):
        """
        Ελέγχει αν έχει περάσει αρκετός χρόνος για να αλλάξει καρέ.
        """
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True 
        
    def get_images(self,path):
        """
       Φορτώνει όλες τις εικόνες για την κίνηση από τον φάκελο.
       
       Args:
           path: Διαδρομή του φακέλου με τις εικόνες.
       
       Returns:
           Μία deque λίστα με όλες τις εικόνες.
       """
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(os.path.join(path, file_name)).convert_alpha()  # Φόρτωση εικόνας.
                images.append(img)
        return images