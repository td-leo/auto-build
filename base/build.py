__author__ = 'xulei'

class build:

    def build(self):
        pass


    def BuildRelease(self):
        self.build()

    def isReadyBuild(self):
        pass


    def deal(self):
        if self.isReadyBuild():
            self.build()


