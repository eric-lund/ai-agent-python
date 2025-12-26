import unittest
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.call_function import call_function
from google.genai import types

class TestFunctions(unittest.TestCase):
    # def test_current_directory(self):
    #     print(f'Results for current directory:\n{get_files_info("calculator",".")}\n')
        
    # def test_pkg_directory(self):
    #     print(f'Results for \'pkg\' directory:\n{get_files_info("calculator","pkg")}\n')

    # def test_bin_filepath(self):
    #     print(f'Results for \'/bin\' directory:\n{get_files_info("calculator", "/bin")}\n')

    # def test_relative_parent_filepath(self):
    #     print(f'Results for \'../\' directory:\n {get_files_info("calculator", "../")}\n')

    # def test_main(self):
    #     print(f'{get_file_content("calculator", "main.py")}')

    # def test_calculator(self):
    #      print(f'{get_file_content("calculator", "pkg/calculator.py")}')

    # def test_bin_cat(self):
    #     print(f'{get_file_content("calculator", "/bin/cat")}')

    # def test_pkg_fake_file(self):
    #     print(f'{get_file_content("calculator", "pkg/does_not_exist.py")}')
   
    # def test_lorem(self):
    #     print(f'{get_file_content("calculator", "lorem.txt")}')

    # def test_write_file_lorem(self):
    #     print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    # def test_write_file_morelorem(self):
    #     print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    
    # def test_write_file_tmp(self):
    #     print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    # def test_run_python_main(self):
    #     print(run_python_file("calculator", "main.py"))

    # def test_run_python_main_args(self):
    #     print(run_python_file("calculator", "main.py", ["3 + 5"]))

    # def test_run_python_calc_test_file(self):
    #     print(run_python_file("calculator", "tests.py"))

    # def test_run_python_calc_main_error(self):
    #     print(run_python_file("calculator", "../main.py"))

    # def test_run_python_calc_nonexistent_error(self):
    #     print(run_python_file("calculator", "nonexistent.py"))

    # def test_run_python_calc_lorem_error(self):
    #     print(run_python_file("calculator", "lorem.txt"))

    # def test_get_files_info_verbose(self):
    #     fake_call = types.FunctionCall(
    #     name="get_files_info",
    #     args={"directory": "."}
    #     )
    #     call_function(fake_call, verbose=True)

    # def test_get_files_info_not_verbose(self):
    #     fake_call = types.FunctionCall(
    #     name="get_files_info",
    #     args={"directory": "."}
    #     )
    #     call_function(fake_call)

    # def test_get_file_content_verbose(self):
    #     fake_call = types.FunctionCall(
    #     name="get_file_content",
    #     args={"file_path": "pkg/calculator.py"}
    #     )
    #     call_function(fake_call, verbose=True)

    def test_wrong_function_name(self):
        fake_call = types.FunctionCall(
        name="get_file_content_",
        args={"file_path": "pkg/calculator.py"}
        )
        call_function(fake_call, verbose=False)


if __name__ == "__main__":
    unittest.main()

