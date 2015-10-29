import sys
from operator import itemgetter
from collections import defaultdict
import heapq

primes = (2,3,5,7,11,13,17,19)
powers = tuple(0 for i in primes)

def compute(primes, powers):
    result = 1
    for i in xrange(len(primes)):
        result *= primes[i] ** powers[i]
    return result

def memoize_unique(fn):
    """Drop already observed values
    """
    fn.output_cache = output_cache = {}
    fn.input_cache = input_cache = {}
    def call(*args):
        if args in input_cache:
            return
        input_cache[args] = True
        out = fn(*args)
        for val in out:
            if val not in output_cache:
                yield val
            output_cache[val] = True
    return call

@memoize_unique
def children(powers, primes=primes):
    c = []
    for i in xrange(len(powers)):
        p = list(powers)
        p[i] += 1
        c.append((compute(primes, p), tuple(p)))
    return c

def gen_value(primes, powers, n=10000):
    primes = tuple(primes)
    initial = children(tuple(powers))
    queue = []
    queue.extend(initial)
    heapq.heapify(queue)
    history = defaultdict(lambda: False)
    i = 1
    while True:
        cost, powers = heapq.heappop(queue)

        if powers in history:
            continue
        else:
            history[powers] = True

        i+=1
        if i >= n:
            return cost

        for child in children(powers):
            heapq.heappush(queue, child)

if __name__ == '__main__':
    input = int(sys.argv[1])
    print (gen_value(primes, powers, input))