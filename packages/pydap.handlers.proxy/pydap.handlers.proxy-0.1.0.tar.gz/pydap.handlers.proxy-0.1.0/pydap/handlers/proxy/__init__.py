import re

from configobj import ConfigObj
from paste.httpexceptions import HTTPSeeOther

from pydap.handlers.lib import BaseHandler
from pydap.exceptions import OpenFileError
from pydap.client import open_url


class Handler(BaseHandler):

    extensions = re.compile(r"^.*\.url$", re.IGNORECASE)

    def __init__(self, filepath):
        self.filepath = filepath

    def parse_constraints(self, environ):
        try:
            config = ConfigObj(self.filepath)
        except:
            message = 'Unable to open file %s.' % self.filepath
            raise OpenFileError(message)
    
        url = config['dataset']['url']
        pass_ = config['dataset']['pass']
        response = environ['pydap.response']

        if response in pass_:
            # forward to the requested response
            raise HTTPSeeOther(url + '.' + response)
        else:
            # load a dataset and return it
            return open_url(url)
