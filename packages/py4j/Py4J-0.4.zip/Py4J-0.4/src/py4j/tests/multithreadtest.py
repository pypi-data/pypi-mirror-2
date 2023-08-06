'''
Created on Sep 17, 2010

@author: barthelemy
'''
from multiprocessing.pool import Pool
from multiprocessing.process import Process
from py4j.java_gateway import JavaGateway
import subprocess
import time
import unittest
from threading import Thread

def start_example_server():
    subprocess.call(["java", "-cp", "../../../../py4j-java/bin/", "py4j.examples.ExampleApplication"])
    
    
def start_example_app_process():
    # XXX DO NOT FORGET TO KILL THE PROCESS IF THE TEST DOES NOT SUCCEED
    p = Process(target=start_example_server)
    p.start()
    return p

class TestJVM1(Thread):
    def __init__(self, gateway):
        Thread.__init__(self)
        self.gateway = gateway
        
    def run(self):
        for i in xrange(3):
            print(self.gateway.jvm.java.lang.System.currentTimeMillis())
            time.sleep(0.5)
            
class TestJVM2(Thread):
    def __init__(self, System):
        Thread.__init__(self)
        self.System = System
        
    def run(self):
        for i in xrange(3):
            print(self.System.currentTimeMillis())
            time.sleep(0.5)
            
class TestJVM3(Thread):
    def __init__(self, jvm):
        Thread.__init__(self)
        self.jvm = jvm
        
    def run(self):
        for i in xrange(3):
            print(self.jvm.java.lang.System.currentTimeMillis())
            time.sleep(0.5)
            
class TestJVM4(Thread):
    def __init__(self, System):
        Thread.__init__(self)
        self.System = System
        
    def run(self):
        print(self.System.currentTimeMillis())
        try:
            self.System.loadLibrary('toto')
        except:
            print('Good!')
        print(self.System.currentTimeMillis())
            
class JVMMultiProcessTest(unittest.TestCase):
    def setUp(self):
#        logger = logging.getLogger("py4j")
#        logger.setLevel(logging.DEBUG)
#        logger.addHandler(logging.StreamHandler())
        self.p = start_example_app_process()
        time.sleep(0.5)
        self.gateway = JavaGateway()
        
    def tearDown(self):
        self.p.terminate()
        self.gateway.shutdown()
        time.sleep(0.5)
        
    def testMultiProcessJVMAccess(self):
        workers = [TestJVM1(self.gateway) for _ in xrange(8)]
        
        for worker in workers:
            worker.start()
            
        for worker in workers:
            worker.join()
            
    def testMultiProcessSystemReference(self):
        System = self.gateway.jvm.java.lang.System
        workers = [TestJVM2(System) for _ in xrange(8)]
        
        for worker in workers:
            worker.start()
            
        for worker in workers:
            worker.join()
            
    def testMultiProcessJVMReference(self):
        jvm = self.gateway.jvm
        workers = [TestJVM3(jvm) for _ in xrange(8)]
        
        for worker in workers:
            worker.start()
            
        for worker in workers:
            worker.join()
            
    def testMultiProcessJVMError(self):
        System = self.gateway.jvm.java.lang.System
        workers = [TestJVM4(System) for _ in xrange(8)]
        
        for worker in workers:
            worker.start()
            
        for worker in workers:
            worker.join()
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testJavaList']
    unittest.main()
        
