from test import *

if __name__ == '__main__':
    pass
    sim1 = RWP2Simulation()
    sim1.simulate()
    c, t, b, n = sim1.summary()
    print(len(sim1.num_of_broadcasters) - 1)
    for i, course in enumerate(t):
        print(i, course)
        if i > 2:
            break
