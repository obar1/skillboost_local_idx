def test_ds(get_ll):
    assert set(["append", "pop", "prepend", "get", "set_value", "remove"]).issubset(
        get_ll.ds_func
    )


def test_constructor(get_ll):
    assert get_ll.get_id == "linked-list"
    assert get_ll.head is not None
    assert get_ll.tail is not None
    assert get_ll.length == 1
    assert str(get_ll) == "ll:['node:0,']"


def test_append(get_ll):
    get_ll.append(1)
    get_ll.append(2)
    assert str(get_ll) == "ll:['node:0,', 'node:1,', 'node:2,']"


def test_pop(get_ll):
    assert str(get_ll.pop()) == "node:0"
    assert str(get_ll.pop()) == "None"


def test_prepend(get_ll):
    get_ll.prepend(2)
    assert str(get_ll) == "ll:['node:2,', 'node:0,']"


def test_get(get_ll):
    assert str(get_ll.get(0)) == "node:0"
    assert str(get_ll.get(1)) == "None"


def test_set_value(get_ll):
    get_ll.set_value(0, "A")
    assert str(get_ll.get(0)) == "node:A"


def test_remove(get_ll3):
    assert str(get_ll3) == "ll:['node:0,', 'node:1,', 'node:2,']"
    get_ll3.remove(1)
    assert str(get_ll3) == "ll:['node:0,', 'node:2,']"
    get_ll3.remove(0)
    assert str(get_ll3) == "ll:['node:2,']"


def test_reverse(get_ll3):
    assert str(get_ll3.reverse()) == "ll:['node:2,', 'node:1,', 'node:0,']"
