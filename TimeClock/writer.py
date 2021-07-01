import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gui import sendWriteRequest
from utilities import getserial

class Writer(threading.Thread):
    def __init__(self, api_url):
        super().__init__()
        # self.reader = SimpleMFRC522()
        self._stop_event = threading.Event()
        self.api_url = api_url
        # self.val = val
        # self.employeeId = employeeId
        # self.read_flag = True
        print("New Writer Class created")    

    def stop(self):
        print('Write thread stopped')
        # GPIO.cleanup()
        self._stop_event.set()

    def resume(self):
        print("Resume")
        self._stop_event.clear()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        if not self._stop_event.is_set():
            try:
                print(threading.current_thread().name)
                GPIO.cleanup()
                print('place to read')
                readerx = SimpleMFRC522()
                id, text = readerx.read()
                GPIO.cleanup()        
                writerx = SimpleMFRC522()
                print("Now place your tag to write")
                writerx.write(self.val)
                # GPIO.setwarnings(False)
                # GPIO.setmode(GPIO.BOARD)
                # buzzer = 11
                # GPIO.setup(buzzer, GPIO.OUT)
                # GPIO.output(buzzer,GPIO.HIGH)
                # time.sleep(2)
                # GPIO.output(buzzer,GPIO.LOW)
                print("Base level Written")
                payload = {'id': id, 'text': self.val, 'device': getserial(), 'employeeId': self.employeeId}
                sendWriteRequest(payload, self.api_url)
            except:
                print('write exception')
                raise
            finally:
                    GPIO.cleanup()
    
    def setWriter(self, val, empId):
        self.val = val
        self.employeeId = empId
        