import redis

if __name__ == '__main__':
    pass
    r = redis.Redis(host='localhost', port=6379, db=0)
    r_set_name = "torus-(50, 0)-100"
    tuples = r.smembers(r_set_name)
    results_list = []
    for tup in tuples:
        tup = eval(tup)
        seed = tup[0]
        results = tup[1]
        results_list.append(results)

    baseline_idx = 0
    better = [0 for _ in range(len(results_list[0]))]
    for results in results_list:
        baseline = results[baseline_idx]
        for i, result in enumerate(results):
            if result < baseline:  # <
                better[i] += 1

    print(better)

    better = [0 for _ in range(len(results_list[0]))]
    for results in results_list:
        baseline = results[baseline_idx]
        for i, result in enumerate(results):
            if result == baseline:  # <
                better[i] += 1

    print(better)

    better = [0 for _ in range(len(results_list[0]))]
    for results in results_list:
        baseline = results[baseline_idx]
        for i, result in enumerate(results):
            if result > baseline:  # <
                better[i] += 1

    print(better)
