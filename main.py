import pygame


class Filter:
    def __init__(self, name):
        self.name = name
        self.img = pygame.Surface((1, 1), pygame.SRCALPHA)

    def load_image(self):
        self.img = pygame.image.load(self.name).convert_alpha()

    def save_image(self, place):
        pygame.image.save(self.img, place)


class GrayScaleTransformer(Filter):
    def __init__(self, name):
        super().__init__(name)

    def transform(self):
        arr = pygame.surfarray.array3d(self.img)

        # print the shape of the array
        print(arr.shape)
        # convert to grayscale using for loops
        for i in range(0, arr.shape[0]):  # column number from 0 to 15
            for j in range(0, arr.shape[1]):  # row number from 0 to 15
                r, g, b = arr[i][j]  # get rgb values for the pixel
                avg = r / 3 + g / 3 + b / 3  # calculate average
                arr[i][j] = [avg, avg, avg]  # set rgb values to average
        self.img = pygame.surfarray.make_surface(arr)


class RGTransformer(Filter):
    def __init__(self, name):
        super().__init__(name)

    def transform(self):
        arr = pygame.surfarray.array3d(self.img)

        # print the shape of the array
        print(arr.shape)
        # convert to grayscale using for loops
        for i in range(0, arr.shape[0]):  # column number from 0 to 15
            for j in range(0, arr.shape[1]):  # row number from 0 to 15
                r, g, b = arr[i][j]  # get rgb values for the pixel
                arr[i][j] = [r, g, 0]  # set rgb values to average
        self.img = pygame.surfarray.make_surface(arr)


# initialize pygame and screen
print('Input file name pls')
image_file = input()+ ".png"
pygame.init()

print('Input new file name pls')
save_file = input()
pygame.init()

screen = pygame.display.set_mode((1200, 400))
transformer = GrayScaleTransformer(image_file)
transformer.load_image()
transformer.transform()
transformer.save_image(save_file + "grey.png")

transformer = RGTransformer(image_file)
transformer.load_image()
transformer.transform()
transformer.save_image(save_file+"rg.png")
