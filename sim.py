from main import *
from redis import Redis

r = Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    pass
    SOURCE_POS = (25, 25)
    for i in range(200):
        RAND_SEED = "%.30f" % time()
        print(i, RAND_SEED)

        MOB = "RWP1"
        sim = RWP1Simulation(RAND_SEED, SOURCE_POS, None)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-ctr",
               str((rd, RAND_SEED)))
        print(rd)

        MOB = "RWP2"
        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, None)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-ctr",
               str((rd, RAND_SEED)))
        print(rd)

        MOB = "RD"
        sim = RDSimulation(RAND_SEED, SOURCE_POS, None)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-ctr",
               str((rd, RAND_SEED)))
        print(rd)

        MOB = "MG1"
        sim = MG1Simulation(RAND_SEED, SOURCE_POS, None)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-ctr",
               str((rd, RAND_SEED)))
        print(rd)

        MOB = "MG2"
        sim = MG2Simulation(RAND_SEED, SOURCE_POS, None)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-ctr",
               str((rd, RAND_SEED)))
        print(rd)
        print()
