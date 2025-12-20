from functions.run_python_file import run_python_file

def test():

    result = run_python_file("calculator", "main.py")
    print(result)

    cal_result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(cal_result)

    cal_success_test = run_python_file("calculator", "tests.py")
    print(cal_success_test)

    error_result = run_python_file("calculator", "../main.py")
    print(error_result)

    failed_py = run_python_file("calculator", "nonexistent.py")
    print(failed_py)

    failed_txt = run_python_file("calculator", "lorem.txt")
    print(failed_txt)

if __name__ == "__main__":
    test()