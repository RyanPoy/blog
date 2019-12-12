#coding: utf8
from .base import *
from settings import MEDIA_ROOT, MEDIA_DIR_NAME


class Image(BaseModel):

    pic = pw.CharField(verbose_name='图片', max_length=255, null=False)

    @property
    def abspath(self):
        return os.path.join(MEDIA_ROOT, self.pic)

    @property
    def url(self):
        return os.path.join('/static', MEDIA_DIR_NAME, self.pic)

    @classmethod
    def my_save(cls, fname, fbody):
        save_name = fname
        while True:
            if cls.get_or_none(cls.pic == save_name):
                save_name = '{}(1)'.format(save_name)
            else:
                break
        save_path = os.path.join(MEDIA_ROOT, save_name)
        with open(save_path, 'wb') as f:
            f.write(fbody)

        obj = cls()
        obj.pic = save_name
        obj.save()
        return obj

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = os.path.getsize(self.abspath)
        return '%.2f KB' % (self._size / 1024.0)

    def to_dict(self):
        d = super().to_dict()
        if os.path.exists(self.abspath):
            d['name'] = self.pic
            d['size'] = self.size
            d['url'] = self.url
        else:
            d['name'] = ''
            d['size'] = 0
            d['url'] = ''
        return d

    def remove(self):
        r = super().remove()
        try:
            os.remove(self.abspath)
        except:
            raise
        return r

    class Meta:
        table_name = 'images'

