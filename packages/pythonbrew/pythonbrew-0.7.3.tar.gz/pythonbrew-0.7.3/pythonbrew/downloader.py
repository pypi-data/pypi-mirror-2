from pythonbrew.define import PYTHON_VERSION_URL, PYTHONBREW_STABLE_VERSION_URL, \
    PYTHONBREW_UPDATE_URL_PYPI, PYTHONBREW_UPDATE_URL_HEAD
from pythonbrew.log import logger
from pythonbrew.curl import Curl
from pythonbrew.util import u

def get_headerinfo_from_url(url):
    c = Curl()
    return c.readheader(url)

def get_stable_version():
    c = Curl()
    return u(c.read(PYTHONBREW_STABLE_VERSION_URL).strip())

class Downloader(object):
    def download(self, msg, url, path):
        logger.info("Downloading %s as %s" % (msg, path))
        c = Curl()
        c.fetch(url, path)

def get_pythonbrew_update_url(version):
    if version == "head":
        return PYTHONBREW_UPDATE_URL_HEAD
    else:
        return PYTHONBREW_UPDATE_URL_PYPI % (version)

def get_python_version_url(version):
    return PYTHON_VERSION_URL.get(version)
