from test import *
from redis import Redis
import statistics

# start from any point, make predictions based on the seed and human intervention
# so that the trace/targets can be adapted to other seeds
# since the increase is exponential, and we can really do nothing when such increase starts
# a strategy is that do a tree search height = 3, set target unit by unit, for 8 direction
# see which 3 steps could produce the most # of influenced cars

r = Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    queries = [
        "E-RWP2-20-20-20-10-10-s0",
        "E-RWP2-20-20-20-10-10-c1s",
    ]
    for q in queries:
        print(q, r.scard(q))
        mem_list = []
        for mem in r.smembers(q):
            mem = eval(mem)
            mem_list.append(mem[0])
        print("avg", sum(mem_list) / len(mem_list))
        # print("stdev", statistics.stdev(mem_list))
        # print("median", statistics.median(mem_list))
        print()
