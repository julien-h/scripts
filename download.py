import urllib
from tqdm import tqdm


class TqdmUpTo(tqdm):
    # https://github.com/tqdm/tqdm/blob/master/examples/tqdm_wget.py
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download(url, filename):
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1) as t:
        return urllib.urlretrieve(url, filename, reporthook=t.update_to)


def download_silent(url, filename):
    return urllib.urlretrieve(url, filename)
