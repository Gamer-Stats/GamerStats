from os.path import splitext
from django.core.files.storage import get_storage_class
from storages.backends.s3boto3 import S3Boto3Storage


class StaticToS3BotoStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        super(StaticToS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage"
        )

    def save(self, name, content):
        ext = splitext(name)[1]
        parent_dir = name.split("/")[0]
        if ext in [".css", ".js"] and not parent_dir == "admin":
            self.local_storage._save(name, content)  # type: ignore
        else:
            filename = super(StaticToS3BotoStorage, self).save(name, content)
            return filename


class CachedS3BotoStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage"
        )

    def save(self, filename, content):
        filename = super(CachedS3BotoStorage, self).save(filename, content)
        self.local_storage._save(filename, content)  # type: ignore
        return filename
