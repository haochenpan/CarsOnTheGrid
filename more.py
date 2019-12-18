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
        "E-RWP1-x50-y50-c25-sx0-sy0-cnr",
        "E-RWP1-x50-y50-c50-sx0-sy0-cnr",
        # "E-RWP2-x50-y50-c25-sx0-sy0-up",
        # "E-RWP2-x50-y50-c25-sx0-sy0-right",
        # "E-RWP2-x50-y50-c25-sx0-sy0-14",
        # "E-RWP2-x50-y50-c25-sx0-sy0-23",
        # "E-RWP2-x50-y50-c25-sx0-sy0-diag",

    ]
    results = []
    for q in queries:
        print(q, r.scard(q))
        mem_list = []
        for mem in r.smembers(q):
            mem = eval(mem)
            mem_list.append(mem[0])
        print("avg", round(sum(mem_list) / len(mem_list), 2))
        results.append(round(sum(mem_list) / len(mem_list), 2))
        # print("stdev", statistics.stdev(mem_list))
        # print("median", statistics.median(mem_list))
    print(*results, sep="\n")
