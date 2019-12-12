#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *


class ImageController(BaseController):

    SUPPORT_IMAGE_TYPES = ('image/jpg', 'image/png', 'image/gif', 'image/jpeg')
    SUPPORT_IMAGE_MAX_SIZE = 500<<10

    def get(self):
        return self.end(data={ 
            'images': [ t.to_dict() for t in Image.select() ]
        })

    @atomic()
    def post(self):
        if 'images' not in self.request.files:
            return self.end(code=-1, err_str='请上传图片')

        for f in self.request.files['images']:
            fname, content_type, fbody = f['filename'], f['content_type'], f['body']
            if content_type.lower() not in self.SUPPORT_IMAGE_TYPES:
                return self.end(code=-1, err_str="只支持JPG、PNG、GIF 图片格式")
            if len(fbody) > self.SUPPORT_IMAGE_MAX_SIZE:
                return self.end(code=-1, err_str="最大支持512KB")
            img = Image.my_save(fname, fbody)
            return self.end(data={
                'image': img.to_dict()
            })

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        img = self.get_object_or_404(Image, id=t.get('id', ''))
        img.remove()
        return self.end(data=img.to_dict())
