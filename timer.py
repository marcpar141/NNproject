import get_db
import time

start_time = time.time()
get = get_db.get_db()

print("%s" % (time.time() - start_time))
