# coding=utf-8
from pint import UnitRegistry

from flack.message import PrivateResponse

from pytest import yield_fixture
from unittest.mock import patch
from fakeredis import FakeStrictRedis
from freezegun import freeze_time

from .. import convert


def _make_redis():
    return FakeStrictRedis(decode_responses=True)


@yield_fixture
def fake_redis():
    with patch.object(convert, "redis", new_callable=_make_redis) as redis:
        yield redis


def test_load_units(fake_redis):
    default_units = convert._load_units()
    assert isinstance(default_units, UnitRegistry)
    assert str(default_units("cm")) == "1 centimeter"

    fake_redis.hset(convert.UNIT_KEY, "foo", "2 centimeter")
    custom_units = convert._load_units()
    assert str(custom_units("cm")) == "1 centimeter"
    assert str(custom_units("foo")) == "1 foo"
    assert str(custom_units("1 foo").to("cm")) == "2.0 centimeter"

    fake_redis.hset(convert.UNIT_KEY, "steve", "__age 2019-01-02")
    with freeze_time("2020-03-04"):
        custom_units = convert._load_units()
    assert str(custom_units("1 steve").to("days")) == "427.0 day"


def test_register_unit(fake_redis):
    result = convert.register_unit("foo2", "1 cm")
    assert isinstance(result, PrivateResponse)
    assert "can only contain letters" in result.feedback

    result = convert.register_unit("foobar", "2 foo")
    assert isinstance(result, PrivateResponse)
    assert "Unknown conversion unit" in result.feedback

    result = convert.register_unit("foo", "2 cm")
    assert "New unit defined: foo" in result
    assert fake_redis.hget(convert.UNIT_KEY, "foo") == "2 centimeter"

    result = convert.register_unit("steve", "birthday 02/01/19")
    assert isinstance(result, PrivateResponse)
    assert "iso-format" in result.feedback

    result = convert.register_unit("steve", "birthday 2019-01-02")
    assert "New unit defined: steve" in result
    assert fake_redis.hget(convert.UNIT_KEY, "steve") == "__age 2019-01-02"


def test_unregister_unit(fake_redis):
    result = convert.unregister_unit("foo")

    assert isinstance(result, PrivateResponse)
    assert "not defined" in result.feedback

    fake_redis.hset(convert.UNIT_KEY, "foo", "2 centimeter")
    result = convert.unregister_unit("foo")
    assert "Removed" in result
    assert not fake_redis.hexists(convert.UNIT_KEY, "foo")


def test_unit_converter():
    with patch.object(convert, "_load_units") as mock_units:
        mock_units.return_value = UnitRegistry()

        # Rounding to two decimal places, strip insignificant zeroes
        assert convert.unit_converter("1 meter", "cm") == "1 meter =~ 100 centimeter"
        assert convert.unit_converter("1 cm", "inch") == "1 centimeter =~ 0.39 inch"
