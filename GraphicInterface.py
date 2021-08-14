
class GraphicInteface():

    def __init__(self, title, geometry, resize, bg, window):
        self.window = window
        self.bgColor = bg if bg is not None else "SystemButtonFace"
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(resize, resize)
        self.window.config(background = bg)