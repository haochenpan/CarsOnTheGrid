from main import *
from redis import Redis

r = Redis(host='localhost', port=6379, db=0)
"""
        sim = RWP2Simulation(seed, (0, 0), [(0, 0)])
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-1staycnr", str((rd, seed)))
        print(rd)

        sim = RWP2Simulation(seed, (25, 25), [(25, 25)])
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-1stayctr", str((rd, seed)))
        print(rd)

        sim = RWP2Simulation(seed, (0, 0), [(1000, 1000)])
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-1diag", str((rd, seed)))
        print(rd)
        
        
        

"""
if __name__ == '__main__':
    pass
