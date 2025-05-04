from sprite_object import* 


class Weapon(AnimatedSprite): # Καλούμε τον κατασκευαστή της κλάσης AnimatedSprite
    def __init__(self,game,path=r"AssetsGame\weapon\0.png",scale =0.4, animation_time = 90):
        super().__init__(game=game,path=path,scale=scale,animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img,(self.image.get_width() * scale,self.image.get_height() * scale))   # Εφαρμόζουμε το scale στις εικόνες του όπλου (δηλαδή, μικραίνουμε/μεγαλώνουμε τις εικόνες)
             for img in self.images]) # Εφαρμόζουμε το scaling σε όλες τις εικόνες του όπλου
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())   # Ορίζουμε την αρχική θέση του όπλου στην οθόνη (στο κέντρο και στο κάτω μέρος)
        self.reloading = False 
        self.num_images = len(self.images) # Αριθμός εικόνων που έχει η ανιμέισον του όπλου
        self.frame_counter = 0   # Μετρητής για τα καρέ της ανιμέισον
        self.damage = 50    # Ζημιά που προκαλεί το όπλο 
        
    def animate_shot(self):
        if self.reloading: # Αν το όπλο είναι σε διαδικασία RELOAD
            self.game.player.shot = False # Απενεργοποιούμε την ένδειξη για πυροβολισμό του παίκτη
            if self.animation_trigger: # Αν υπάρχει σήμα για να εκτελέσουμε την ανιμέισον
                self.images.rotate(-1) # Κάνουμε περιστροφή στις εικόνες για να εμφανιστεί η επόμενη
                self.image = self.images[0] # Ορίζουμε την τρέχουσα εικόνα από την πρώτη στη λίστα
                self.frame_counter += 1 # Αυξάνουμε τον μετρητή καρέ
                if self.frame_counter == self.num_images: # Αν έχουμε ολοκληρώσει όλα τα καρέ
                    self.reloading = False  # Ολοκληρώθηκε reload
                    self.frame_counter = 0  # Επαναφέρουμε τον μετρητή καρέ
                    
        
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
        
    def update(self):
        self.check_animation_time()
        self.animate_shot()