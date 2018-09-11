from datetime import datetime

import pytest

from pyFixedFlatFile import PyFixedFlatFile
from pyFixedFlatFile.exceptions import ParamsException


@pytest.fixture
def setup_empty():
    return PyFixedFlatFile()


@pytest.fixture
def setup_eq(setup_empty):
    setup_empty.eq("10")

    return setup_empty


# Tests for normal situations
def test_only_size_param(setup_eq):
    """size must be equal to positional numeric param passed to the attribute"""
    setup_eq.id(2)
    assert setup_eq.data == {"10": [{'ident': 'id', 'size': 2}]}


def test_size_and_default_params(setup_eq):
    setup_eq.inscricaoEstadual(14, default='')
    assert setup_eq.data == {
        "10": [{'ident': 'inscricaoEstadual', 'size': 14, 'default': ''}]}


def test_size_and_tp_params(setup_eq):
    """tp value must be numeric"""
    setup_eq.fax(10, tp='numeric')
    assert setup_eq.data == {
        "10": [{'ident': 'fax', 'size': 10, 'tp': 'numeric'}]}


def test_fmt_param_is_callable(setup_eq):
    """fmt value must be a callable"""
    setup_eq.dataInicial(8, fmt=lambda d: format(d, '%d%m%Y'))
    assert callable(setup_eq.data["10"][0]['fmt'])


def test_format_method_with_size_only(setup_eq):
    reg = {"id": "10"}
    spec = {'ident': 'id', 'size': 2}
    assert setup_eq.fmt(spec, reg) == '10'


def test_format_method_with_fmt(setup_eq):
    reg = {
        "dataInicial": datetime.now()
    }
    spec = {'ident': 'dataInicial', 'size': 8,
            'fmt': lambda d: format(d, '%d%m%Y')}
    assert setup_eq.fmt(spec, reg) == datetime.now().strftime('%d%m%Y')

# Tests for errors situations


def test_only_size_param_with_invalid_value(setup_eq):
    """size must be a int number otherwise a exception must be raised"""
    with pytest.raises(ParamsException):
        setup_eq.id('10')


def test_tp_invalids_values(setup_eq):
    """tp must be only 'numeric' value otherwise a exception must be raised"""
    with pytest.raises(ParamsException):
        setup_eq.fax(10, tp='')


def test_fmt_param_is_not_callable(setup_eq):
    """fmt value must be a callable otherwise a exception must be raised
    """
    with pytest.raises(ParamsException):
        setup_eq.dataInicial(8, fmt="lambda d : format(d, '%d%m%Y')")


def test_format_method_with_size_only_error(setup_eq):
    reg = {"id": "10"}
    spec = {'ident': 'id', 'size': 10}
    with pytest.raises(Exception):
        assert setup_eq.fmt(spec, reg) == '10'


def test_format_method_with_fmt(setup_eq):
    reg = {
        "dataInicial": datetime.now()
    }
    spec = {'ident': 'dataInicial', 'size': 2,
            'fmt': lambda d: format(d, '%d%m%Y')}
    with pytest.raises(Exception):
        assert setup_eq.fmt(spec, reg) == datetime.now().strftime('%d%m%Y')

def test_multiplous_named_params():
    """default, fmt and tp must be combined?"""
    assert True


def test_spec_without_id():
    """Ainda preciso implementar"""
    assert True
