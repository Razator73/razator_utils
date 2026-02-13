#!/usr/bin/env python

"""Tests for `razator_utils` package."""
from pathlib import Path

import pytest

from razator_utils import batchify, camel_to_snake, log, flatten_dict


def test_camel_to_snake():
    """Test the camel_to_snake function which converts camelCase to snake_case"""
    assert camel_to_snake('thisIsTest') == 'this_is_test'
    assert camel_to_snake('anotherATest') == 'another_a_test'


def test_batchify():
    iterable = ['a', 'b', 'c', 'd', 'e']
    assert [x for x in batchify(iterable, 2)] == [['a', 'b'], ['c', 'd'], ['e']]


def test_stout_log():
    logger = log.get_stout_logger('pytest.py', 'INFO')
    assert logger.level == 20
    log_file = Path('test.log')
    file_logger = log.get_file_logger('pytest_file_log.py', log_file, 'WARNING')
    file_logger.warning('This is a warning')
    assert log_file.exists()
    log_file.unlink()


@pytest.mark.parametrize('test_data,expected', [
    ({}, {}),
    ({'not_nested': 'dictionary'}, {'not_nested': 'dictionary'}),
    ({'single': {'nested': 'dict'}}, {'single_nested': 'dict'}),
    (
        {'single': {'nested': 'dict'}, 'multiple': {'key1': 'val1', 'key2': 'val2'}},
        {'single_nested': 'dict', 'multiple_key1': 'val1', 'multiple_key2': 'val2'}
     ),
    (
        {'single': {'nested': 'dict'}, 'multiple': {'dict1': {'key1': 'val1'}, 'key2': 'val2'}},
        {'single_nested': 'dict', 'multiple_dict1_key1': 'val1', 'multiple_key2': 'val2'}
    ),
    (
        {'triple': {'nested': {'dictionary': 'val'}}},
        {'triple_nested_dictionary': 'val'}
    ),
    (({'single': {'nested': 'dict'}}, '', '.'), {'single.nested': 'dict'}),
    (({'single': {'nested': 'dict'}}, 'flat', '.'), {'flat.single.nested': 'dict'}),
])
def test_flatten_dict(test_data, expected):
    if isinstance(test_data, tuple):
        pass
    else:
        assert flatten_dict(test_data) == expected


def test_get_chrome_major_version():
    from razator_utils.razator_utils import get_chrome_major_version
    from unittest.mock import patch

    # Test success case
    with patch('shutil.which') as mock_which, \
         patch('subprocess.check_output') as mock_subprocess:

        mock_which.side_effect = lambda x: '/usr/bin/google-chrome' if x == 'google-chrome' else None
        mock_subprocess.return_value = b'Google Chrome 120.0.6099.109'

        version = get_chrome_major_version()
        assert version == 120

    # Test binary not implemented found
    with patch('shutil.which') as mock_which, \
         patch('platform.system') as mock_system:

        mock_which.return_value = None
        mock_system.return_value = 'Linux'

        version = get_chrome_major_version()
        assert version is None

    # Test subprocess error
    with patch('shutil.which') as mock_which, \
         patch('subprocess.check_output') as mock_subprocess:

        mock_which.return_value = '/usr/bin/google-chrome'
        mock_subprocess.side_effect = Exception("Command failed")

        version = get_chrome_major_version()
        assert version is None


def test_discord_message():
    from razator_utils.razator_utils import discord_message
    from unittest.mock import patch
    import pytest

    webhook_url = "https://discord.com/api/webhooks/1234567890/TOKEN"
    text = "Hello, Discord!"

    # Test success
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 204

        discord_message(webhook_url, text)

        mock_post.assert_called_once_with(webhook_url, json={"content": text})

    # Test failure
    with patch('requests.post') as mock_post:
        import requests
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Client Error")

        with pytest.raises(Exception) as excinfo:
            discord_message(webhook_url, text)

        assert "Failed to send Discord message" in str(excinfo.value)


def test_cli_or_file_logger():
    # Test CLI (verbose=True)
    logger = log.cli_or_file_logger('test_cli', verbose=True)
    assert logger.name == 'test_cli'
    assert len(logger.handlers) > 0
    assert any(isinstance(h, log.logging.StreamHandler) for h in logger.handlers)

    # Test File (verbose=False)
    test_log = Path('test_file_logger.log')
    if test_log.exists():
        test_log.unlink()

    logger = log.cli_or_file_logger('test_file', verbose=False, log_path=test_log)
    assert logger.name == 'test_file'
    assert test_log.exists()

    # Cleanup
    test_log.unlink()


def test_redirect_stdout_to_logger():
    import logging
    from unittest.mock import MagicMock
    from razator_utils.log import redirect_stdout_to_logger

    mock_logger = MagicMock(spec=logging.Logger)
    mock_logger.info = MagicMock()

    with redirect_stdout_to_logger(mock_logger, level="INFO"):
        print("Test message 1")
        print("Test message 2")

    mock_logger.info.assert_any_call("Test message 1")
    mock_logger.info.assert_any_call("Test message 2")
