class Alien:
    health = 3
    alien_counter = 0

    def __init__(self, x_cor=0, y_cor=0):
        self.x_coor = x_cor
        self.y_coor = y_cor
        Alien.alien_counter += 1

    def hit(self):
        self.health -= 1



alien = Alien(2, 0)
print(alien.health)
alien.hit()
print(alien.health)
