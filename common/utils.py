from django.core.files.storage import FileSystemStorage


class MediaFileSystemStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(MediaFileSystemStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        import hashlib
        import os

        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        # md5sum as file name
        md5 = hashlib.md5(content.read()).hexdigest()
        # rewrite directory
        d = os.path.join(d, md5[:1], md5[1:2])
        # rewrite filename
        fn = md5
        # rewrite file full path
        name = os.path.join(d, fn + ext)

        if self.exists(name):
            return name

        return super(MediaFileSystemStorage, self)._save(name, content)
