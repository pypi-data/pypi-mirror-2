import sys
import os.path

pwd = os.path.dirname(__file__)
if pwd:
    pilpe_path = os.path.abspath(os.path.dirname(__file__)+"/../")
else:    
    pilpe_path = os.path.abspath(os.path.dirname(__file__)+"..")
sys.path.append(pilpe_path)

from pilpe import Pipeline
from pilpe.plugins import OCR, PDF

#images_path = '%s/test/data/' % (pilpe_path)
images_path = []
images_path.append('%s/test/data/page1.tif' % (pilpe_path))
images_path.append('%s/test/data/page2.tif' % (pilpe_path))

ocr = OCR({'lang': 'por'})

pdf = PDF({
    'path': pilpe_path+'/test/pdfsaver.pdf', 
    'title': 'Projeto de lei - No. 912742', 
})

pipeline = Pipeline()
pipeline.register(ocr)
pipeline.register(pdf)
pipeline.run(images_path)
