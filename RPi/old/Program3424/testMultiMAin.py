from multiprocessing import Process
from time import sleep
from multiprocessing import Event
class test_multi(Process):
    def __init__(self, ext):
        Process.__init__(self)
        self.ok =12
        self.exss = ext

    def run(self):
        while not self.exss.is_set():
            sleep(1)
            self.ok = self.ok + 1
            print(self.ok)
        print('bye')


if __name__ == '__main__':

    exit_flag = Event()
    test = test_multi(exit_flag)

    test.start()

    run = True

    while run:
        inp = input(' ')

        if inp == 's':
            exit_flag.set()

        if inp == 'q':
            run = False