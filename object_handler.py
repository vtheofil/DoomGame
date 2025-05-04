from sprite_object import * 
from npc import*
from random import choices,randrange  # Εισαγωγή της συνάρτησης choices για τυχαία επιλογή και randrange για τυχαία θέση

class ObjectHandler:
    def __init__(self,game):
        self.game = game 
        self.sprite_list=[] # Λίστα για τα στατικά ή animated sprites
        self.npc_list = [] # Λίστα για τους NPC
        self.npc_sprite_path = r"AssetsGame\npc"  # Διαδρομή για τα sprites των NPC
        self.static_sprite_path =r"AssetsGame\sprites\static_sprites" # Διαδρομή για τα στατικά sprites
        self.anim_sprite_path = r"AssetsGame\animatedSprites"  # Διαδρομή για τα animated sprites
        add_sprite = self.add_sprite  # Σύντομος τρόπος για να καλέσουμε τη συνάρτηση προσθήκης sprite
        add_npc = self.add_npc  # Σύντομος τρόπος για να καλέσουμε τη συνάρτηση προσθήκης NPC
        self.npc_positions = {}  # Λεξικό για τις θέσεις των NPC
        
        # spawn npc
        self.enemies = 10  # npc count
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC] # Λίστα με τους τύπους NPC
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # Περιοχή που δεν επιτρέπεται για spawn NPC
        self.spawn_npc()
        
        
        
        #stripe map
       # add_sprite(SpriteObject(game))
       # add_sprite(AnimatedSprite(game))
       # add_sprite(AnimatedSprite(game, pos=(1.5,1.5)))
       # add_sprite(AnimatedSprite(game, pos=(1.5,7.5)))
       # add_sprite(AnimatedSprite(game, pos=(5.5,3.25)))
       # add_sprite(AnimatedSprite(game, pos=(5.5,4.75)))
       # add_sprite(AnimatedSprite(game, pos=(7.5,2.5)))
       # add_sprite(AnimatedSprite(game, pos=(7.5,5.5)))
       # add_sprite(AnimatedSprite(game, pos=(14.5,1.5)))
        add_sprite(AnimatedSprite(game , path=self.anim_sprite_path + r"\redLight\0.png", pos =(14.5, 7.5))) # Κωδικοποιούνται sprites που εμφανίζονται στον κόσμο, για παράδειγμα, κόκκινα φώτα
        add_sprite(AnimatedSprite(game , path=self.anim_sprite_path + r"\redLight\0.png", pos =(12.5, 7.5)))
        add_sprite(AnimatedSprite(game , path=self.anim_sprite_path + r"\redLight\0.png", pos =(9.5, 7.5)))
        
        #npc map
        add_npc(NPC(game))    
        add_npc(NPC(game,pos=(11.5,4.5))) # Παράδειγμα προσθήκης NPC με θέση
        
        # Προσθήκη διάφορων τύπων NPC με θέσεις
        add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        add_npc(SoldierNPC(game, pos=(4.0, 29.0)))
        add_npc(CacoDemonNPC(game, pos=(5.5, 14.5)))
        add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))
        add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))
        
    def spawn_npc(self):
        # Δημιουργία NPC τυχαία με βάση weights και θέσεις
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows) # Επιλογή τυχαίας θέσης
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):  # Εξασφαλίζει ότι το NPC δεν θα εμφανιστεί σε περιοχές με τοίχους ή περιορισμένες περιοχές
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5))) # Δημιουργία NPC και προσθήκη στη λίστα

    def check_win(self):
        # Έλεγχος για το αν έχει κερδίσει ο παίκτης (αν δεν υπάρχουν NPC στον κόσμο)
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()  # Ενημέρωση οθόνης
            pg.time.delay(1500) # Καθυστέρηση για 1,5 δευτερόλεπτα
            self.game.new_game()   
    
    
    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive} 
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()
        
    def add_npc(self,npc):
        self.npc_list.append(npc)

        
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
