import matplotlib.pyplot as plot

class Plotter():
    def __init__(self):
        self.figure = plot.figure()
        self.axis = self.figure.add_subplot(111)
        self.line = [[],[]]
        self.points = [[], []]
        plot.ion()
        plot.show()

    def append_to_line(self, coordinates):
        self.line[0].append(coordinates[0])
        self.line[1].append(coordinates[1])

    def change_points(self, points):
        self.points = points

    def draw_updates(self):
        self.axis.clear()
        self.axis.plot(*self.line, color='red')
        self.axis.scatter(*self.points, color='blue')
        plot.draw()
        plot.pause(1)

if (__name__ == "__main__"):
    plotter = Plotter()
    plotter.append_to_line([1, 1])
    plotter.change_points([[0,0], [1, 1]])
    plotter.change_points([[0,0], [0.5, 0.5]])
    plotter.change_points([[0,0], [1, 2]])
    plotter.append_to_line([1, 2])
    input()
