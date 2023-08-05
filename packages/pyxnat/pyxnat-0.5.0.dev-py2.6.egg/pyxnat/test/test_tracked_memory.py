import tempfile

from pyxnat.tracked_memory import TrackedMemory


memory = TrackedMemory(tempfile.gettempdir())

@memory.cache
def func_fixed_args(arg1, arg2):
    return arg1, arg2

@memory.cache
def func_args(*args):
    return args

@memory.cache
def func_kwargs(**kwargs):
    return kwargs


def test_fixed():
    assert func_fixed_args('1', '2') == ('1', '2')
    assert func_fixed_args('5', '4') == ('5', '4')
    assert func_fixed_args.tracks == [(('1', '2'), {}), (('5', '4'), {})]

def test_args():
    assert func_args('1', '2', ['pouet', 'pouetpouet']) == ('1', '2', ['pouet', 'pouetpouet'])
