# coding=utf-8
from unittest.mock import patch

from .. import command_convert, command_define
from .. import convert


def test_command_convert():
    response = command_convert("")
    assert "usage" in response.feedback

    with patch.object(convert, "unit_converter") as mock_converter:
        mock_converter.return_value = "1 foo = 2 bar"
        response = command_convert("1 foo to bar")

        assert response == "1 foo = 2 bar"
        mock_converter.assert_called_with("1 foo", "bar")


def test_command_define():
    response = command_define("")
    assert "usage" in response.feedback

    with patch.object(convert, "register_unit") as mock_register:
        mock_register.return_value = "Defined foobar"
        response = command_define("1 foo = 2 bar")

        assert response == "Defined foobar"
        mock_register.assert_called_with("1 foo", "2 bar")

    with patch.object(convert, "unregister_unit") as mock_unregister:
        mock_unregister.return_value = "Removed foobar"
        response = command_define("-u foobar")

        assert response == "Removed foobar"
        mock_unregister.assert_called_with("foobar")
