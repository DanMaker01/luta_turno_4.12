class GameLogic:
    def __init__(self, timeline):
        self.timeline = timeline
        self.t = 0

    def update(self):
        self.timeline.update()
        self.t += 1
        if self.t % 50 == 0:  # tempo de um turno in_game
            self.timeline.addTimeline()