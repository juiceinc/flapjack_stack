import os
import pytest

from flapjack_stack import FlapjackStack

COOKIE_SETTING = 'cookie are awesome'


class TestFlapjackStack:

    def test_push_layer_from_py_file(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/test-stacks.py')
        assert COOKIE_SETTING == flapjacks.COOKIE_SETTING

    def test_push_layer_from_yaml_file(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/test-stacks.yaml')
        assert COOKIE_SETTING == flapjacks.COOKIE_SETTING

    def test_push_layer_from_yml_file(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/test-stacks.yml')
        assert COOKIE_SETTING == flapjacks.COOKIE_SETTING

    def test_push_layer_from_invalid_yaml_file(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/invalid.yaml')
        with pytest.raises(AttributeError):
            flapjacks.COOKIE_SETTING

    def test_push_layer_from_missing_yaml_file(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/missing.yaml')
        with pytest.raises(AttributeError):
            flapjacks.COOKIE_SETTING

    def test_push_layer_from_unsupported_file(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/test-stacks.txt')
        with pytest.raises(AttributeError):
            flapjacks.COOKIE_SETTING

    def test_add_and_remove(self):
        flapjacks = FlapjackStack()
        flapjacks.COOKIES = 'chocolate chip'
        assert 'chocolate chip' == flapjacks.COOKIES
        flapjacks.add_layer()
        flapjacks.COOKIES = 'chocolate chip, peanut butter'
        assert 'chocolate chip, peanut butter' == flapjacks.COOKIES
        flapjacks.remove_layer()
        assert 'chocolate chip' == flapjacks.COOKIES

    def test_load_from_environment(self):
        flapjacks = FlapjackStack()
        flapjacks.add_layer_from_file('./tests/test-stacks.py')
        os.environ['FJS_COOKIE_SETTING'] = "eat all the cookies"
        flapjacks.add_layer_from_env()
        assert "eat all the cookies" == flapjacks.COOKIE_SETTING
