import pytest
from src.nodes import Node
from src.linked_lists import  LinkedList
 
 
@pytest.fixture
def get_node():
    return Node(0)

@pytest.fixture
def get_ll():
    return LinkedList(0)

@pytest.fixture
def get_ll3():
    ll= LinkedList(0)
    ll.append(1)
    ll.append(2)
    return ll