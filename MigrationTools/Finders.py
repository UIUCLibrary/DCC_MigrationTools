import os
import re
import pickle


def check_valid(func):
    def call_func(*args, **kwargs):
        path = args[1]
        if not os.path.exists(path):
            raise FileNotFoundError("Path \"{}\" not found.".format(path))

        return func(*args, **kwargs)
    return call_func

@check_valid
def find_file_locally(filename, path):
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if file_ == filename:
                yield os.path.join(root, file_)


class PickeledFinder:
    def __init__(self, cache_file=None):
        self._tree = None
        self._cached_file = cache_file

        if self._cached_file is not None:
            self.load(self._cached_file)

    @check_valid
    def map_path(self, path):
        self._tree = list(os.walk(path))

    def walk(self):
        if self._tree is None:
            raise Exception("No data loaded")
        return self._tree

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self._tree, f)
        pass

    def load(self, filename):
        with open(filename, "rb") as f:
            self._tree = pickle.load(f)
        pass



class CachedFinder:
    @check_valid
    def __init__(self, path):
        self._tree = []
        for item in os.walk(path):
            self._tree.append(item)

    def find_file(self, filename, case_insensitive=False):
        results = []
        for root, dirs, files in self._tree:
            for file_ in files:
                if case_insensitive:
                    if file_.lower() == filename.lower():
                        results.append(os.path.join(root, file_))
                else:
                    if file_ == filename:
                        results.append(os.path.join(root, file_))
        return results

    def regex_matches(self, regex):
        pattern = re.compile(regex, re.IGNORECASE)
        results = []

        for root, dirs, files in self._tree:
            for file_ in files:
                if re.match(pattern, file_):
                    results.append(os.path.join(root, file_))
        return results