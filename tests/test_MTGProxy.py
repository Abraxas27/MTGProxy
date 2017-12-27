import MTGProxy
import os
import pytest
# import param
from unittest.mock import patch, call
import shutil


@pytest.fixture(scope='session')
def param():
    pass


def test_adapt_regex_if_land():
    assert MTGProxy.adapt_regex_if_land('forest (v.1)', 'forest (v.1)') == 'forest\s?\(v\.\s?1\)'
    # assert MTGProxy.adapt_regex_if_land('forest (v.1)', 'FOREST (v.1)') == 'forest\s?\(v\.\s?1\)'
    assert MTGProxy.adapt_regex_if_land('forest v.1', 'forest v.1') == 'forest v.1'
    assert MTGProxy.adapt_regex_if_land('damnation', 'damnation') == 'damnation'
    assert MTGProxy.adapt_regex_if_land('huatli, warrior poet', 'Huatli, Warrior Poet') == 'huatli, warrior poet'


# def test_copy_card(tmpdir):
#     start_id = 1
#     MTGProxy.current_proxy_id = start_id
#     param.OUTPUT_PROXY_DIR = tmpdir
#     mock_path = '/some/path'
#     quantity = 4
#     with patch('shutil.copy'):
#         MTGProxy.copy_card(mock_path, quantity)
#         for i in range(0, quantity):
#             file_output = os.path.join(tmpdir, str(start_id + i) + '.jpg')
#             shutil.copy.assert_has_calls([call('/some/path', file_output)], any_order=True)
#     assert MTGProxy.current_proxy_id == start_id + quantity


def test_is_double_faced_card():
    param.CARDS_DOUBLE_FACED = {"Hired Muscle": "Scarmaker"}
    assert MTGProxy.is_double_faced_card("Hired Muscle") is True
    assert MTGProxy.is_double_faced_card("Fake Test") is False


# def test_delete_older_work(tmpdir_factory):
#     # Create OUTPUT_DIR part
#     param.OUTPUT_DIR = tmpdir_factory.mktemp('output')
#     param.OUTPUT_PROXY_DIR = os.path.join(param.OUTPUT_DIR, 'Proxy')
#     # Create CONF_DIR part
#     param.CONF_DIR = tmpdir_factory.mktemp('conf')
#     open(os.path.join(param.CONF_DIR, 'Proxy.sla'), 'w').close()
#     # os.mkdir(param.OUTPUT_PROXY_DIR)
#     # mock NOT_FOUND_FILE
#     param.NOT_FOUND_FILE = os.path.join(param.OUTPUT_DIR, "not_found.txt")
#
#     def assert_initial_directories():
#         assert os.path.exists(param.OUTPUT_PROXY_DIR)
#         assert os.path.exists(param.NOT_FOUND_FILE)
#         assert os.path.exists(os.path.join(param.OUTPUT_DIR, param.OUTPUT_FILE_NAME))
#
#     param.OUTPUT_FILE_EXTENSION = '.sla'
#     param.OUTPUT_FILE_NAME = 'Proxy.sla'
#     MTGProxy.delete_older_work()
#     assert_initial_directories()
#     open(os.path.join(param.OUTPUT_PROXY_DIR, '22.jpg'), 'w').close()


    # os.path.join(param.OUTPUT_DIR, "not_found.txt")
    # MTGProxy.delete_older_work()
