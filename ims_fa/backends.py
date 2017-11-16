# -*- coding:UTF-8 -*-

from qiniustorage import backends
from django.utils.encoding import filepath_to_uri
from six.moves.urllib_parse import urljoin
from django.conf import settings


class QiniuStorage(backends.QiniuStorage):
    def url(self, name):
        name = self._normalize_name(self._clean_name(name))
        name = filepath_to_uri(name)
        bucket_domain2 = settings.QINIU_BUCKET_DOMAIN2
        bucket_name2=settings.QINIU_BUCKET_NAME2
        protocol = 'https://' if self.secure_url else 'http://'
        if name.startswith("baoma/20"):
            url = urljoin(protocol + self.bucket_domain, name)
        else:
            url = urljoin(protocol + bucket_domain2, bucket_name2+name)
        return url