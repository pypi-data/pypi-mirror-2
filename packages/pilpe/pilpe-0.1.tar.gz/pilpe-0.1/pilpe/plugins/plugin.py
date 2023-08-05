class Plugin(object):
    def __init__(self, config={}):
        raise NotImplementedError

    def run(self, image_list=None):
        raise NotImplementedError
