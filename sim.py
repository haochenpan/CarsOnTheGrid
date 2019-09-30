from main import *
from redis import Redis

r = Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    SOURCE_POS = (0, 0)
    for i in range(1):
        RAND_SEED = "%.30f" % time()
        print(i, RAND_SEED)
        MOB = "RWP2"

        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, None)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-up",
               str((rd, RAND_SEED)))
        print(rd)
        gui = GUINumBro(sim, True, False)
        gui.draw()
        gui.save("ctr")

        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, RWP2_up())
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-up",
               str((rd, RAND_SEED)))
        print(rd)
        gui = GUINumBro(sim, True, False)
        gui.draw()
        gui.save("up")


        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, RWP2_right())
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-up",
               str((rd, RAND_SEED)))
        print(rd)
        gui = GUINumBro(sim, True, False)
        gui.draw()
        gui.save("right")

        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, RWP2_zigzag_14())
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-up",
               str((rd, RAND_SEED)))
        print(rd)
        gui = GUINumBro(sim, True, False)
        gui.draw()
        gui.save("14")

        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, RWP2_zigzag_23())
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-up",
               str((rd, RAND_SEED)))
        print(rd)
        gui = GUINumBro(sim, True, False)
        gui.draw()
        gui.save("23")

        sim = RWP2Simulation(RAND_SEED, SOURCE_POS, RWP2_diagonal())
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-sx{SOURCE_POS[0]}-sy{SOURCE_POS[1]}-up",
               str((rd, RAND_SEED)))
        print(rd)
        gui = GUINumBro(sim, True, False)
        gui.draw()
        gui.save("diag")

