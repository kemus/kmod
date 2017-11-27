import collections
import concurrent.futures
import hashlib
import functools
import os
import zlib
from progress import progress

# from ctypes import windll, create_string_buffer

# Quick size shortcuts
K = 1024
M = K*K

cache_limit = 1024*1024
cache = {}


def get_hash_key(filename, size=None):
    """Calculates the hash value for a file."""
    hash_object = hashlib.sha256()
    for chunk in chunk_reader(filename, max_size=size):
        hash_object.update(chunk)
    return hash_object.digest()

def get_crc_key(filename, size=None):
    """Calculates the crc value for a file."""
    crc = None
    for chunk in chunk_reader(filename, max_size=size):
        if not crc:
            crc = zlib.adler32(chunk)
        else:
            crc = zlib.adler32(chunk, crc)
    return crc

def get_size_key(filename):
    try:
        size = os.path.getsize(filename)
    except:
        size = -1
    return size

def get_mod_path(filename):
    try:
        _, mod, path = filename.split(os.sep, 2)
    except ValueError as e:
        print(filename + " should be made to be in ascii")
        raise e
    return mod, path
tuple_mapper = lambda i, func: (i, func(i))




class Checker(object):
    def __init__(self, base):
        self.base = base
        self.cache_limit = 32*K



    def comparison(self, name, func, num_checks, input):
        checked = 0
        out = collections.defaultdict(lambda : collections.defaultdict(list))
        futures = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Start the read operations and mark each future with its filepath
            for path, values in input.items():
                for mods in values.values():
                    # don't bother if last round didn't have duplicates
                    if len(mods) <= 1:
                        continue
                    for mod in mods:
                        filepath = os.path.join(self.base, mod, path)
                        futures[executor.submit(func, filepath)] = (mod, path)

            for future in concurrent.futures.as_completed(futures):
                mod, path = futures[future]
                key = future.result()
                out[path][key].append(mod)
                checked += 1
                progress(checked, num_checks, name)

        dupes = 0
        with open('_%s.txt', 'w') as f:
            with open('_%s_conflicts.txt', 'w') as fc:
                for path, values in out.iteritems():
                    for key, mods in values.iteritems():
                        key_str = ','.join([path, str(key)] + mods) + '\n'
                        f.write(key_str)
                        if len(mods) > 1:
                            dupes += len(mods)
                            fc.write(key_str)
        return dupes, out

    def check_for_duplicates(self):
        mods = collections.defaultdict(lambda: collections.defaultdict(list))
        num_dupes = 0
        for dirpath, dirnames, filenames in os.walk(self.base):
            for name in filenames:
                filename = os.path.join(dirpath, name)
                if 'meta.ini' in filename or '.txt' in filename or 'fomod' in filename:
                    continue
                mod, path = get_mod_path(filename)
                mods[path][None].append(mod)
                if len(mods[path][None]) == 2:
                    num_dupes += 2
                if len(mods[path][None]) > 2:
                    num_dupes += 1
        num_dupes, mods = self.comparison('size', get_size_key, num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('crc8K', functools.partial(get_crc_key, size=1*K), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('crc32K', functools.partial(get_crc_key, size=4*K), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('crc32K', functools.partial(get_crc_key, size=32*K), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('hash32K', functools.partial(get_hash_key, size=32*K), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('hash128K', functools.partial(get_hash_key, size=128*K), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('hash1M', functools.partial(get_hash_key, size=1*M), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('hash16M', functools.partial(get_hash_key, size=16*M), num_dupes, mods)
        if num_dupes == 0:
            return
        num_dupes, mods = self.comparison('hash', get_hash_key, num_dupes, mods)

if __name__ == '__main__':
    checker = Checker('mods')
    checker.check_for_duplicates()
