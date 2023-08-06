"""Local File System product"""
__doc__="""Local File System product"""

from ZPublisher.Iterators import filestream_iterator
from OFS.Image import File

class StreamingFile(File):
    """ wrapper around OFS.Image.File that does streaming from the file"""
    def index_html(self, REQUEST, RESPONSE, path):
        """    XXX FIXME: this doesn't have range support etc.
               Note: this relies on _wrap_ob(self) having been called by now.
        """
        threshold = 2 << 16 # 128 kb
        if self.size < threshold or RESPONSE is None:
            try:
                f = open(self._local_path, 'rb')
                return f.read()
            finally:
                f.close()
        else:
            RESPONSE.setHeader('Content-Length', self.size)
            RESPONSE.setHeader('Content-Type', self.content_type)
            return filestream_iterator(path, 'rb')
