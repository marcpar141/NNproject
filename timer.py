import get_bin
import time

"""
In this example (actually made for timing this methods) 
we are using path to binary data db/nose.bin.
Also type of data we want to withdraw, image as matix
You can use this to test between Python versions and Pypy.
Between Python 3.8 and Pypy was difference of about 0.7sec! to load and ptint data
"""
start_time = time.time()
get = get_bin.get_bin("D://Repos/NNproject/NNsite/db/ant.bin")

print("%s" % (time.time() - start_time))
print(get.data["image"])
print(get.data["key_id"])
