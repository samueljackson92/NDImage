import sklearn.manifold
import sklearn.decomposition
import inspect


class AlgorithmFactory(object):

    @staticmethod
    def create(name, parameters={'n_components': 2}):
        class_ = AlgorithmFactory.get_algorithm_class(name)
        return class_(**parameters)

    @staticmethod
    def get_algorithm_class(name):
        if hasattr(sklearn.decomposition, name):
            module = sklearn.decomposition
        elif hasattr(sklearn.manifold, name):
            module = sklearn.manifold
        else:
            raise ValueError("Unsupported algorithm: %s " % name)

        return getattr(module, name)

    @staticmethod
    def get_algorithm_parameters(name):
        class_ = AlgorithmFactory.get_algorithm_class(name)
        func_args = inspect.getargspec(class_.__init__.im_func)
        func_values = func_args.defaults
        func_names = func_args.args[-len(func_values):]
        return zip(func_names, func_values)
