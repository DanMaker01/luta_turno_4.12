class GameLogic:
    def __init__(self, timeline, database):
        self.timeline = timeline
        self.database = database
        
        
        self.t = 0
        

    def update(self):
        self.timeline.update()
        self.t += 1
        if self.t % self.database.TEMPO == 0:  # tempo para atualizar um turno no jogo
            self.timeline.addTimeline()
            