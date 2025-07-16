from functions.run_python import run_python_file


def test_one():
    result = run_python_file("calculator", "main.py")
    print(result)
    assert 'Usage' in result

def test_two():
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    assert '8' in result

def test_three():
    result = run_python_file("calculator", "tests.py")
    print(result)
    assert 'Ran' in result

def test_four():
    result = run_python_file("calculator", "../main.py")
    print(result)
    assert 'Error' in result

def test_five():
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    assert 'Error' in result


# Run the tests when the file is executed directly
if __name__ == "__main__":
    test_one()
    print()
    test_two()
    print()
    test_three()
    print()
    test_four()
    print()
    test_five()
    print()