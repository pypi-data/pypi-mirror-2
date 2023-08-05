from plugin import Plugin
from reportlab.pdfgen import canvas

class PDF(Plugin):
    def __init__(self, config):
        self.path = config.get('path')
        self.title = config.get('title')
    
    def run(self, images):
        c = canvas.Canvas(self.path)

        for image in images:
            width, height = pagesize = image.size
            c.setPageSize(pagesize)
            
            image_text = image.info['pilpe'].get('ocr')
            if image_text is not None:
                y = height - 30
                for line in image_text.split('\n'):
                    c.drawString(30, y, line)
                    y -= 15        
    
            c.drawInlineImage(image, 0, 0)
            c.showPage()

        if self.title is not None:
            c.setTitle(self.title)

        c.save()

        return images
