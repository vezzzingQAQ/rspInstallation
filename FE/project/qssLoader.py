class CommonQssLoader:
    @staticmethod
    def readCss(style):
        with open(style,"r") as f:
            return f.read()