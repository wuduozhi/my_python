import pytest

@pytest.fixture(scope="module")
def foo(request):
    print('\nfoo setup - module fixture')
    def fin():
        print('\nfoo teardown - module fixture')
    request.addfinalizer(fin)
 
@pytest.fixture()
def bar(request):
    print('\nbar setup - function fixture')
    def fin():
        print('\nbar teardown - function fixture')
    request.addfinalizer(fin)
 
@pytest.fixture()
def baz(request):
    print('\nbaz setup - function fixture')
    def fin():
        print('\nbaz teardown - function fixture')
    request.addfinalizer(fin)
 
def test_one(foo,bar,baz):
    print('in test_one()\n')
 
def test_two(foo,bar,baz):
    print('in test_two()\n')