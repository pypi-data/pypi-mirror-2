import os
import Image

class Pipeline(object):
    def __init__(self):
        self.__plugins = []
    
    def register(self, plugin):
        self.__plugins.append(plugin)
    
    def run(self, image_path):
        images = []
        if type(image_path) == list:
            for file in image_path:
                try:
                    images.append(Image.open(file))
                except Exception, e:
                    # TODO: Log warning
                    # Some files may not be valid image files
                    pass

        elif os.path.isdir(image_path):
            for file in os.listdir(image_path):
                try:
                    images.append(Image.open(image_path+'/'+file))
                except Exception, e:
                    # TODO: Log warning
                    # Some files may not be valid image files
                    pass
        
        else:
            images.append(Image.open(image_path))

        if len(images) == 0:
            return None

        [ image.info.update({'pilpe': {}}) for image in images ] 

        for plugin in self.__plugins:
            result = plugin.run(images)
            images = result
        return images  
        
