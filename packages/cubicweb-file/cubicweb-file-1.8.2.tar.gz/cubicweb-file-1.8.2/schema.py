_ = unicode

# pylint: disable-msg=E0611,F0401
from yams.buildobjs import EntityType, String, Bytes
try:
    from yams.buildobjs import RichString
except ImportError:
    from cubicweb.schema import RichString

class File(EntityType):
    """a downloadable file which may contains binary data"""
    title = String(fulltextindexed=True, maxsize=256)
    data = Bytes(required=True, fulltextindexed=True,
                 description=_('file to upload'))
    data_format = String(required=True, meta=True, maxsize=50,
                         description=_('MIME type of the file. Should be dynamically set at upload time.'))
    data_encoding = String(meta=True, maxsize=20,
                           description=_('encoding of the file when it applies (e.g. text). '
                                         'Should be dynamically set at upload time.'))
    data_name = String(required=True, fulltextindexed=True, maxsize=128,
                       description=_('name of the file. Should be dynamically set at upload time.'))
    description = RichString(fulltextindexed=True, internationalizable=True,
                             default_format='text/rest')


class Image(File):
    """a file typed as an image"""
