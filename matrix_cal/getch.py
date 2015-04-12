class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import tty, sys, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

if __name__ == "__main__":
    """little testing, for arrow up"""
    def testArrow():
        getint = lambda: ord(getch())
        a = getint()
        if a != 27:
            print a
            return
        b = getint()
        if b != 91:
            print a,b
            return
        c = getint()
        if c == 65:
            print "Up"
            return
        if c == 66:
            print "Down"
            return 
        if c == 67:
            print "Right"
            return
        if c == 68:
            print "Left"
            return
        print a,b,c
    
    testArrow()
            
