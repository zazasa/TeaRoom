from django.db import models

# Create your models here.


class AbstractUploader(object):
    
    def __init__(self, arg):
        super(AbstractUploader, self).__init__()
        print '>>>>>> UPLOADER'
        