class Alien:
    health = 3
    alien_counter = 0

    def __init__(self, x_cor=0, y_cor=0):
        self.x_coor = x_cor
        self.y_coor = y_cor
        Alien.alien_counter += 1

    def hit(self):
        self.health -= 1

    def is_alive(self):
        return (self.health > 0)

    def teleport(self, new_x, new_y):
        self.x_coor = new_x
        self.y_coor = new_y

    def collision_detection(self, other_alien):
        pass

    def total_aliens_created(self):
        return Alien.alien_counter


def new_aliens_collection(coordinates):
    aliens = []
    for i in coordinates:
        aliens.append(Alien(i[0], i[1]))
    return aliens


alien = Alien(2, 0)
print(alien.health)
alien.hit()
print(alien.health)
