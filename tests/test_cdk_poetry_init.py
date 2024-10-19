import os
import pytest
import subprocess
import sys
from unittest import mock
from cdk_poetry_init import run_command, create_file, create_readme

# Test run_command
def test_run_command_success():
    with mock.patch("subprocess.Popen") as mock_popen:
        mock_process = mock.Mock()
        mock_popen.return_value = mock_process
        mock_process.communicate.return_value = (b'output', b'')
        mock_process.returncode = 0

        output = run_command('dummy command')
        assert output == 'output'
        mock_popen.assert_called_once_with('dummy command',
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           shell=True
                                           )


def test_run_command_failure():
    with mock.patch("subprocess.Popen") as mock_popen, mock.patch("sys.exit") as mock_exit:
        mock_process = mock.Mock()
        mock_popen.return_value = mock_process
        mock_process.communicate.return_value = (b'', b'error')
        mock_process.returncode = 1

        run_command('dummy command')
        mock_popen.assert_called_once_with('dummy command', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        mock_exit.assert_called_once_with(1)


# Test create_file
def test_create_file():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        create_file("test.txt", "file content")
        mock_file.assert_called_once_with("test.txt", 'w')
        mock_file().write.assert_called_once_with("file content")


# Test create_readme
def test_create_readme():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file, mock.patch("cdk_poetry_init.create_file") as mock_create_file:
        create_readme("test_project")
        mock_create_file.assert_called_once_with("README.md", mock.ANY)
        assert "Welcome to your CDK Python project!" in mock_create_file.call_args[0][1]
