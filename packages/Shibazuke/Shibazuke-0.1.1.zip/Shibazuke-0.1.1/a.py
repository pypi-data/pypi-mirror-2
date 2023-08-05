import shibazuke

import time
#a = ['a'*(i % 4096) for i in xrange(2**14)]
a = range(1024) * 2**10

f = time.clock()
shibazuke.dumps(a)
print time.clock()-f