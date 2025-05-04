from sprite_object import*
from random import randint, random,choice


class NPC(AnimatedSprite):
    """
   Κλάση για τους μη παικτικούς χαρακτήρες (NPC) που κληρονομεί από την AnimatedSprite.
   """
    def __init__(self, game,path= r"AssetsGame\npc\soldier\0.png",pos=(10.5, 5.5),
                 scale = 0.6 , shift=0.38 , animation_time = 180):
        super().__init__(game,path,pos,scale,shift,animation_time)
        # Φόρτωση εικόνων για διάφορες καταστάσεις του NPC
        self.attack_images = self.get_images(r"AssetsGame\npc\soldier\attack")
        self.death_images = self.get_images(r"AssetsGame\npc\soldier\death")
        self.idle_images = self.get_images(r"AssetsGame\npc\soldier\idle")
        self.pain_images = self.get_images(r"AssetsGame\npc\soldier\pain")
        self.walk_images = self.get_images(r"AssetsGame\npc\soldier\walk")
        # Ιδιότητες NPC
        self.attack_dist = randint(3,6)   # Τυχαία απόσταση από την οποία μπορεί να επιτεθεί.
        self.speed= 0.03 # Ταχύτητα κίνησης του NPC
        self.size = 10   # Μέγεθος του NPC για ανίχνευση σύγκρουσης
        self.health = 100 # Ζωή του NPC.
        self.attack_damage = 10  # Ζημιά που προκαλεί όταν επιτίθεται
        self.accuracy = 0.15   # Ακρίβεια επίθεσης
        self.alive = True  # Αν ο NPC είναι ζωντανός
        self.pain = False   # Αν ο NPC δέχεται ζημιά
        self.ray_cast_value = False  # Αν ο παίκτης είναι ορατός μέσω ανίχνευσης ακτίνας
        self.frame_counter = 0  # Μετρητής καρέ για την αναπαραγωγή της κίνησης
        self.player_search_trigger = False  # Αν ο NPC αναζητά τον παίκτη
        
    def update(self):
        """
        Ενημερώνει την κατάσταση του NPC σε κάθε καρέ.
        """
        self.check_animation_time()  # Ελέγχει αν πρέπει να αλλάξει καρέ animation
        self.get_sprite()  # Υπολογίζει τη θέση του sprite στην οθόνη
        self.run_logic()   # Εκτελεί τη λογική του NPC (κίνηση, επίθεση κ.λπ.)
        
    def check_wall(self,x,y):
        """
       Ελέγχει αν μια θέση (x, y) είναι τοίχος.
       """
        return(x,y) not in self.game.map.world_map # Επιστρέφει True αν δεν είναι τοίχος

    
    def check_wall_collision(self,dx,dy):
        """
       Ελέγχει και αποτρέπει σύγκρουση του NPC με τοίχο.
       """
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx   # Ενημερώνει τη θέση στον άξονα x αν δεν υπάρχει σύγκρουση
        if self.check_wall(int(self.x), int(self.y +dy * self.size)):
            self.y += dy   # Ενημερώνει τη θέση στον άξονα y αν δεν υπάρχει σύγκρουση
        
    def movement(self):
        """
       Υπολογίζει την κίνηση του NPC προς τον παίκτη.
       """
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos) # Υπολογίζει το επόμενο βήμα
        next_x, next_y = next_pos   # Εξάγει τις συντεταγμένες του επόμενου βήματος
        if next_pos  not in self.game.object_handler.npc_positions:  # Ελέγχει αν το επόμενο βήμα είναι ελεύθερο
            angle = math.atan2(next_y +0.5 - self.y, next_x +0.5 - self.x) # Υπολογίζει τη γωνία προς το επόμενο βήμα
            dx = math.cos(angle) * self.speed # Υπολογίζει τη μετακίνηση στον x
            dy = math.sin(angle) * self.speed # Υπολογίζει τη μετακίνηση στον y
            self.check_wall_collision(dx,dy) # Ελέγχει συγκρούσεις πριν μετακινηθεί
            
    def attack(self):
        """
       Εκτελεί επίθεση στον παίκτη αν βρίσκεται εντός εμβέλειας.
       """
        if self.animation_trigger: # Ελέγχει αν είναι ώρα για επίθεση με βάση το animation
            self.game.sound.npc_shot.play()  # Παίζει ήχο επίθεσης
            if random() < self.accuracy: # Ελέγχει αν η επίθεση είναι επιτυχής με βάση την ακρίβεια
                self.game.player.get_damage(self.attack_damage) # Προκαλεί ζημιά στον παίκτη
         
    
    def animate_death(self):
        """
       Παίζει την κινούμενη εικόνα θανάτου του NPC.
       """
        if not self.alive:   # Ελέγχει αν το NPC είναι νεκρό
            if self.game.global_trigger and self.frame_counter < len ( self.death_images)- 1:  # Ελέγχει τον αριθμό καρέ
                self.death_images.rotate(-1)  # Αλλάζει την εικόνα του animation
                self.image = self.death_images[0]  # Ορίζει την επόμενη εικόνα
                self.frame_counter += 1 # Αύξηση του μετρητή καρέ
    
    
    def animate_pain(self):
        """
        Παίζει την κινούμενη εικόνα όταν ο NPC δέχεται ζημιά.
        """
        self.animate(self.pain_images) # Χρησιμοποιεί τις εικόνες πόνου για animation
        if self.animation_trigger:  # Όταν τελειώσει το καρέ πόνου
            self.pain= False  # Απενεργοποιεί την κατάσταση πόνου 
        
    def check_hit_in_npc(self):
        """
        Ελέγχει αν ο NPC έχει δεχτεί χτύπημα από τον παίκτη.
        """
        if self.ray_cast_value and self.game.player.shot:  # Ελέγχει ορατότητα και αν ο παίκτης πυροβόλησε
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage # Μειώνει την ζωή του NPC
                self.check_health()  # Ελέγχει αν πρέπει να πεθάνει το NPC
                
    def check_health(self):
        """
       Ελέγχει αν ο NPC είναι ζωντανός ή πέθανε.
       """
        if self.health < 1:  # Αν η υγεία του είναι 0 ή λιγότερο
            self.alive = False  # Ο NPC πεθαίνει
            self.game.sound.npc_death.play()  # Παίζει ήχο θανάτου του NPC
        
    def run_logic(self):
        """
        Επεξεργάζεται τη λογική του NPC, όπως κινήσεις, επιθέσεις και αντιδράσεις.
        """
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc() # Ελέγχει αν ο παίκτης είναι ορατός
            self.check_hit_in_npc() # Ελέγχει αν δέχτηκε χτύπημα
            
            if self.pain:  # Αν ο NPC πονάει
                self.animate_pain() 
                
            elif self.ray_cast_value: # Αν ο NPC βλέπει τον παίκτη
                self.player_search_trigger = True
                if self.dist < self.attack_dist: # Αν είναι κοντά στον παίκτη
                    self.animate(self.attack_images) # Παίζει την επίθεση
                    self.attack()
                else: # Αν είναι μακριά από τον παίκτη
                    self.animate(self.walk_images) # Παίζει την κίνηση
                    self.movement()
                
            elif self.player_search_trigger: # Αν ο NPC έχει ξεκινήσει να ψάχνει τον παίκτη
                self.animate(self.walk_images) # Παίζει την κίνηση
                self.movement()
                
            else:
                self.animate(self.idle_images) # Παίζει την ακινησία
        else: # Αν ο NPC έχει πεθάνει
            self.animate_death()
                
                
    @property
    def map_pos(self):
        """
       Επιστρέφει τη θέση του NPC στον χάρτη.
       """
        return int(self.x), int (self.y)
    
    def ray_cast_player_npc(self):
        """
      Υπολογίζει αν ο παίκτης είναι ορατός από τον NPC μέσω ανίχνευσης ακτίνας.
      """
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_dist_v, wall_dist_h = 0,0
        player_dist_v, player_dist_h = 0,0
        
        
        ox,oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        
        ray_angle = self.theta
        
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        
        y_hor,dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1 )
        
        depth_hor = (y_hor - oy) / sin_a
        x_hor= ox + depth_hor * cos_a

        delta_depth = dy / sin_a 
        dx = delta_depth * cos_a
        
        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy 
            depth_hor += delta_depth 
            

        
        x_vert , dx = (x_map + 1,1) if cos_a > 0 else (x_map - 1e-6, -1)
        
        depth_vert = (x_vert - ox) /cos_a
        y_vert = oy + depth_vert * sin_a
        
        delta_depth = dx / cos_a 
        dy = delta_depth * sin_a 
        
        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy 
            depth_vert += delta_depth
            
        player_dist = max(player_dist_v,player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)
        
        if 0<player_dist < wall_dist or not wall_dist:
            return True
        return False
        # Υποκατηγορίες NPC με διαφορετικές παραμέτρους
class SoldierNPC(NPC):
    """
   NPC τύπου στρατιώτης.
   """
    def __init__(self, game, path=r"AssetsGame\npc\soldier\0.png", pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

class CacoDemonNPC(NPC):
    """
NPC τύπου CacoDemon.
"""

    def __init__(self, game, path=r"AssetsGame\npc\cacoDemon\0.png", pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(r"AssetsGame\npc\cacoDemon\attack")
        self.death_images = self.get_images(r"AssetsGame\npc\cacoDemon\death")
        self.idle_images = self.get_images(r"AssetsGame\npc\cacoDemon\idle")
        self.pain_images = self.get_images(r"AssetsGame\npc\cacoDemon\pain")
        self.walk_images = self.get_images(r"AssetsGame\npc\cacoDemon\walk")
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35

class CyberDemonNPC(NPC):
    """
   NPC τύπου CyberDemon.
   """
    def __init__(self, game, path=r"AssetsGame\npc\cyberDemon\0.png", pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(r"AssetsGame\npc\cyberDemon\attack")
        self.death_images = self.get_images(r"AssetsGame\npc\cyberDemon\death")
        self.idle_images = self.get_images(r"AssetsGame\npc\cyberDemon\idle")
        self.pain_images = self.get_images(r"AssetsGame\npc\cyberDemon\pain")
        self.walk_images = self.get_images(r"AssetsGame\npc\cyberDemon\walk")
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25