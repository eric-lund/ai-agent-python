import unittest
from functions.get_files_info import get_files_info

class TestFunctions(unittest.TestCase):
    def test_current_directory(self):
        print(f'Results for current directory:\n{get_files_info("calculator",".")}\n')
        
    def test_pkg_directory(self):
        print(f'Results for \'pkg\' directory:\n{get_files_info("calculator","pkg")}\n')

    def test_bin_filepath(self):
        print(f'Results for \'/bin\' directory:\n{get_files_info("calculator", "/bin")}\n')

    def test_relative_parent_filepath(self):
        print(f'Results for \'../\' directory:\n {get_files_info("calculator", "../")}\n')

if __name__ == "__main__":
    unittest.main()