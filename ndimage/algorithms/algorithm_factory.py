import sklearn.manifold
import sklearn.decomposition


class AlgorithmFactory(object):

    @staticmethod
    def create(name, parameters={'n_components': 2}):
        print name
        if hasattr(sklearn.decomposition, name):
            module = sklearn.decomposition
        elif hasattr(sklearn.manifold, name):
            module = sklearn.manifold
        else:
            raise ValueError("Unsupported algorithm: %s " % name)

        class_ = getattr(module, name)
        return class_(**parameters)
