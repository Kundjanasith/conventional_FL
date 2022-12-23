import sys, os, time, glob, copy
from threading import Thread
sys.path.insert(1, '..')       
import utils

while True:
    utils.receive_model('0.0.0.0',19191)
    # c = Thread(target=utils.receive_model, args=('0.0.0.0',19191))
    # c.run()