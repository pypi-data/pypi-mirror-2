#! /usr/bin/env python

import sys
def main():
    try:
        import nts.ntsWX
        nts.ntsWX.main()
    except:
        print('Errors importing nts.ntsWX ')
        print(sys.exc_info())

if __name__ == "__main__":
    main()