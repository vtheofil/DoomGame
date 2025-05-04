import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self,game):
        self.game = game  # Σύνδεση με το αντικείμενο του παιχνιδιού
        self.ray_casting_result = []  # Αρχικοποίηση του αποτελέσματος του raycasting
        self.objects_to_render = []  # Αρχικοποίηση της λίστας των αντικειμένων προς εμφάνιση
        self.textures = self.game.object_renderer.wall_textures  # Φορτώνουμε τις υφές των τοίχων
    
    def get_objects_to_render(self): # Μέθοδος για να πάρουμε τα αντικείμενα που πρέπει να εμφανιστούν στην οθόνη
        self.objects_to_render = [] # Επαναφορά της λίστας των αντικειμένων προς εμφάνιση
        for ray, values in enumerate(self.ray_casting_result): # Για κάθε ακτίνα που έχουμε υπολογίσει
            depth, proj_height, texture, offset = values  # Αποσπάμε τα δεδομένα από το αποτέλεσμα του raycasting
            
            if proj_height < HEIGHT: # Αν το ύψος του τοίχου είναι μικρότερο από την οθόνη
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),0,SCALE,TEXTURE_SIZE # Κόβουμε την υφή του τοίχου στο κατάλληλο τμήμα
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height)) # Κάνουμε αναδιάσταση για να ταιριάξει στο ύψος του τοίχου
                wall_pos = (ray * SCALE, HALF_HEIGHT-proj_height // 2) # Ορισμός θέσης τοίχου στην οθόνη
            else: # Αν το ύψος του τοίχου είναι μεγαλύτερο από το ύψος της οθόνης
                # Υπολογίζουμε το ύψος του τοίχου αναλογικά με την οθόνη
                texture_height = TEXTURE_SIZE *HEIGHT /proj_height 
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),HALF_TEXTURE_SIZE - texture_height // 2, 
                    SCALE, texture_height
                    )
                wall_column = pg.transform.scale(wall_column, (SCALE,HEIGHT))  # Κάνουμε αναδιάσταση για να ταιριάξει στο ύψος της οθόνης
                wall_pos = (ray * SCALE, 0) # Ορισμός θέσης τοίχου στην οθόνη
                
            
            
            self.objects_to_render.append((depth,wall_column,wall_pos)) # Προσθέτουμε το αποτέλεσμα του τοίχου στη λίστα των αντικειμένων προς εμφάνιση

            
    def ray_cast(self): # Μέθοδος για το raycasting, που υπολογίζει την απόσταση και την υφή του κάθε τοίχου
        self.ray_casting_result = [] # Επαναφέρουμε τα αποτελέσματα του raycasting
        ox,oy = self.game.player.pos # Παίρνουμε την τρέχουσα θέση του παίκτη
        x_map, y_map = self.game.player.map_pos # Παίρνουμε τη θέση του παίκτη στον χάρτη
        
        ray_angle = self.game.player.angle - HALF_FOV +0.0001  # Υπολογίζουμε τη γωνία για την πρώτη ακτίνα
        for ray in range(NUM_RAYS):  # Για κάθε ακτίνα
            sin_a = math.sin(ray_angle)  # Υπολογίζουμε το ημίτονο της γωνίας
            cos_a = math.cos(ray_angle) # Υπολογίζουμε τη θέση της οριζόντιας ακτίνας στον άξονα Χ
            
            y_hor,dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1 ) # Ανάλογα με την κατεύθυνση της ακτίνας
             
            depth_hor = (y_hor - oy) / sin_a  # Υπολογίζουμε το βάθος της οριζόντιας ακτίνας
            x_hor= ox + depth_hor * cos_a  # Υπολογίζουμε τη θέση της οριζόντιας ακτίνας στον άξονα Χ

            delta_depth = dy / sin_a  # Διαφορά βάθους
            dx = delta_depth * cos_a  # Διαφορά στην θέση Χ ανά μονάδα βάθους
            
            for i in range(MAX_DEPTH):  # Αναζητούμε μέχρι το μέγιστο βάθος
                tile_hor = int(x_hor), int(y_hor) # Υπολογίζουμε το tile που βρίσκεται η ακτίνα
                if tile_hor in self.game.map.world_map: # Αν το tile υπάρχει στον χάρτη
                    texture_hor = self.game.map.world_map[tile_hor] # Παίρνουμε την υφή του τοίχου
                    break
                # Αν δεν βρήκαμε τοίχο, συνεχίζουμε την ακτίνα
                x_hor += dx
                y_hor += dy 
                depth_hor += delta_depth 
                

             # Υπολογισμός για την κάθετη ακτίνα
            x_vert , dx = (x_map + 1,1) if cos_a > 0 else (x_map - 1e-6, -1)
            
            depth_vert = (x_vert - ox) /cos_a
            y_vert = oy + depth_vert * sin_a
            
            delta_depth = dx / cos_a 
            dy = delta_depth * sin_a 
            
            for i in range(MAX_DEPTH): # Αναζητούμε μέχρι το μέγιστο βάθος
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map: # Αν το tile υπάρχει στον χάρτη
                    texture_vert = self.game.map.world_map[tile_vert]  # Παίρνουμε την υφή του τοίχου
                    break
                # Αν δεν βρήκαμε τοίχο, συνεχίζουμε την ακτίνα
                x_vert += dx
                y_vert += dy 
                depth_vert += delta_depth
                
            # Ελέγχουμε ποια ακτίνα (οριζόντια ή κάθετη) έχει μικρότερο βάθος (αυτός είναι ο πιο κοντινός τοίχος)
            if depth_vert < depth_hor:
                depth,texture = depth_vert, texture_vert
                y_vert %= 1  # Υπολογισμός του offset για την υφή
                offset= y_vert if cos_a>0 else (1 - y_vert)
            else:
                depth,texture = depth_hor, texture_hor
                x_hor %= 1  # Υπολογισμός του offset για την υφή
                offset = (1-x_hor) if sin_a > 0 else x_hor
            
            depth *= math.cos(self.game.player.angle - ray_angle) # Εφαρμόζουμε διόρθωση βάθους για την απόσταση
        
            #PROJECTION
            proj_height = SCREEN_DIST /(depth + 0.0001)
           
            #ray casting result
            self.ray_casting_result.append((depth,proj_height,texture,offset)) 
            
            ray_angle += DELTA_ANGLE # Αυξάνουμε την γωνία για την επόμενη ακτίνα
    
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()