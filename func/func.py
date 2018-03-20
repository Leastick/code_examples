def fit_to_segment(x, left_board, right_board):
    if x < left_board:
        return left_board
    if x > right_board:
        return right_board
    return x


def hamming_distance(first_hash, second_hash):
    return bin((first_hash ^ second_hash)).count('1')


def ignore_exception(exception=Exception, value=None):
    def wrapper(function):
        def func(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                return value
        return func
    return wrapper


tryparse_int = ignore_exception(ValueError)(int)
tryparse_float = ignore_exception(ValueError)(float)


@ignore_exception(ValueError)
def tryfind(current_list, element):
    index = current_list.index(element)
    return index


def get_name_from_path(path):
    return path.split('/')[-1]
