# Mama mIA aka MarIA Kart

# AI Training (1/3)
# env : gestion du jeu simulé  
# Issu du Notebook3

# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi
# Thibaud Le Du - Gaspard Lauras

from model import Model
from render import Rendering

class CarEnv:
    
    def __init__(self,nomFond):
        self.game = Model() 
        self.nomFond = nomFond                                                    # model.py
        self.screen = None
        
    
    def seed (self, seed):
        self.game.seed(seed)
        
    def reset(self):
        self.game.init(self.nomFond)
        if self.screen: self.screen.init()
        state = self.game.state()
        return state

    def step(self, flapped):   
        self.game.act(flapped)  
        reward = self.game.update()
        state = self.game.state()
        return state, reward, self.game.game_over(), None
           
    def render(self, mode=None):
        if not self.screen:
            self.screen = Rendering(self.game)                                  # render.py
            self.screen.init()
        frame = self.screen.render()
        return frame
               
    def close(self):
        if self.screen: 
            self.screen.render()
            self.screen.close()
            self.screen = None