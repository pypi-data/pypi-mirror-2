from fanstatic.config import convert_config
from fanstatic import make_injector, make_publisher, make_fanstatic

def test_convert_config():
    d = {
        'hashing': 't',
        'devmode': 'false',
        'bottom': 'True',
        'force_bottom': 'False',
        'rollup': 0,
        'somethingelse': 'True',
        }
    assert convert_config(d) == {
        'hashing': True,
        'devmode': False,
        'bottom': True,
        'force_bottom': False,
        'rollup': False,
        'somethingelse': 'True',
        }

def test_injector_config():
    d = {
        'hashing': 't',
        'devmode': 'false',
        'bottom': 'True',
        'force_bottom': 'False',
        'rollup': 0,
        }
    injector = make_injector(None, {}, **d)
    assert injector.app is None
    assert injector.config == {
        'hashing': True,
        'devmode': False,
        'bottom': True,
        'force_bottom': False,
        'rollup': False,
        }

def test_publisher_config():
    publisher = make_publisher(None,  {}, publisher_signature='foo')
    assert publisher.trigger == '/foo/'
    assert publisher.app is None

def test_fanstatic_config():
    d = {
        'hashing': 't',
        'devmode': 'false',
        'bottom': 'True',
        'force_bottom': 'False',
        'rollup': 0,
        'publisher_signature': 'foo',
        }
    fanstatic = make_fanstatic(None, {}, **d)
    assert fanstatic.trigger == '/foo/'
    assert fanstatic.app.config == {
        'hashing': True,
        'devmode': False,
        'bottom': True,
        'force_bottom': False,
        'rollup': False,
        'publisher_signature': 'foo',
        }

