from unittest.mock import patch
import Settings

class mock_test(object):
    @patch('Settings.DT','f')
    def foo(self):
        print(Settings.DT)

def main():
    m = mock_test()
    m.foo()

if __name__ == main():
    main()