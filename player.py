import settings


class Player:

    def __init__(self, name, player):
        self.name = name
        self.player_type = player
        if self.player_type == "Mario":
            self.pic_left = "images\\sml.png"
            self.pic_right = "images\\smr.png"
        elif self.player_type == "Luigi":
            self.pic_left = "images\\lml.png"
            self.pic_right = "images\\lmr.png"
        elif self.player_type == "Bowser":
            self.pic_left = "images\\bml.png"
            self.pic_right = "images\\bmr.png"
        elif self.player_type == "Wario":
            self.pic_left = "images\\wml.png"
            self.pic_right = "images\\wmr.png"
        elif self.player_type == "Other":
            self.pic_left = settings.fnamep
            self.pic_right = settings.fnamep
        elif self.player_type == "Other1":
            self.pic_left = settings.fnamep1
            self.pic_right = settings.fnamep1
        elif self.player_type == "Other2":
            self.pic_left = settings.fnamep2
            self.pic_right = settings.fnamep2
        elif self.player_type == "Other3":
            self.pic_left = settings.fnamep3
            self.pic_right = settings.fnamep3
