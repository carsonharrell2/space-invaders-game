class GameStats():
    """track the statistics of alien invasion"""

    def __init__(self, ai_settings):
        """initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        self.game_active = False

        try:
            with open('high_score.json') as f:
                high_score = int(f.read())
        except ValueError:
            self.high_score = 0
        else:
            self.high_score = high_score

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1


