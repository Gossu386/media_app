def test_add_two():
    x = 1 
    y = 2
    assert x + y == 3

def test_dict_contains():
    x = {"a": 1, "b":2}

    expected = {"a":2, "b": 2}

    assert expected.items() <= x.items()
