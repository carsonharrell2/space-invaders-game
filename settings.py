class Settings():
    """a class to store all of the settings"""

    def __init__(self):
        """initialize the games settings"""
        self.screen_width = 630
        self.screen_height = 450
        self.bg_color = (0, 230, 230)

        # ship settings
        self.ship_speed_factor = 100
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # alien settings
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.2

        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that will change throughout the game"""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 10
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


