import argparser

from menu import print_context


# Shouldn't print anything with no input
def test_print_context_none(capsys):
    print_context()
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


# Indicate that verbosity is on
def test_print_context_verb(capsys, monkeypatch):
    monkeypatch.setattr(argparser.cmdargs, 'verbosity', True)
    print_context()
    out, err = capsys.readouterr()
    assert out == '[*] Verbosity switch is on\n\n\n'
    assert err == ''
