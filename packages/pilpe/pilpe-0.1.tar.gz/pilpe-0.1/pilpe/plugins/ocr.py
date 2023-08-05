import subprocess
import os
import random
from plugin import Plugin
from datetime import datetime
import tempfile

TESSERACT_BIN = 'tesseract' # Name of executable to be called at command line

class OCR(Plugin):
    def __init__(self, config):
        self.lang = config.get('lang')  

    def run(self, images):
        for image in images:
            image_text = self.__image_to_string(image)
            image.info['pilpe']['ocr'] = image_text
        return images

    def __randstr(self, lenght=8, charset='abcdefghijklmnopqrstuvxywz0123456789'):
        """Generates a random string"""
    
        password = []
        for i in range(lenght):
            rand = random.randint(0,len(charset)-1)
            password.append(charset[rand])
    
        return "-" + "".join(password)
    
    def __call_tesseract(self, scratch_image, output):
        """Calls external tesseract on input file (restrictions on types),
        outputting output+'txt'"""
        args = [TESSERACT_BIN, scratch_image, output]
        if self.lang is not None:
            args.append('-l')
            args.append(self.lang)
    
        proc = subprocess.Popen(args)
        retcode = proc.wait()
    
    def __image_to_string(self, image, cleanup = False):
        """Converts im to file, applies tesseract, and fetches resulting text.
        If cleanup=True, delete scratch files after operation."""
        
        current_sec = datetime.today().strftime("%s")
        rand = self.__randstr(8)
        scratch_image = tempfile.mkstemp('.tif')[1]
        output = tempfile.mkstemp('.txt')[1]
        
        try:
            self.__image_to_scratch(image, scratch_image)
            self.__call_tesseract(scratch_image, output[:-4])
            fp = open(output)
            txt = fp.read()
            fp.close()
        finally:
            if cleanup:
                self.__perform_cleanup(scratch_image, output)
        return txt
    
    def __image_to_scratch(self, image, scratch_image):
        """Saves image in memory to scratch file. '.tif' format will be read correctly by Tesseract"""
        image = image.convert('L')
        image.save(scratch_image, dpi=(200,200), compression=None)
         
    def __perform_cleanup(self, scratch_image, output):
        """Clean up temporary files from disk"""
        for name in (scratch_image, output+'.txt'):
            try:
                os.remove(name)
            except OSError:
                pass
    
