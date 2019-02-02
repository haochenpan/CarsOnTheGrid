"""
    Generates after simulation:
        Grid object, Broadcaster object, Stats, Config Snapshot
    Generate during GUI call:
        Grid object -> Plotting positions (for the first round)
        Plotting positions -> Line spaces (for all animations)
        Grid object -> Colors (for all rounds)
        Grid object -> Source's positions on the second graph
"""
from collections import defaultdict
from threading import Thread, Event
from time import sleep, time
from queue import Empty, Queue
from pymongo import MongoClient
import pickle
import main
import helplib
from gui import Gui


class Simulation:
    def __init__(self):
        self.on_going = Event()
        self.data_queue = Queue()
        self.batch_vol = 50
        self.simulator_num = 4
        self.db_writer_num = 4
        self.simulation_ctr = 0  # a approx counter due to race condition
        self.simulation_tme = time()
        self.collection = MongoClient()['CarsOnTheGrid']['r20c20n1000r100']

    def db_writer(self, name):
        write_list = []
        while self.on_going.is_set():
            approx_qsize = self.data_queue.qsize()
            print(f"{name} says approx_qsize is", approx_qsize)
            for i in range(self.batch_vol):
                try:
                    write_list.append(self.data_queue.get_nowait())
                except Empty:
                    break
                except Exception as e:
                    repr(e)
            if len(write_list) > 0:
                # print(f"{name} is inserting")
                self.collection.insert_many(write_list)
                write_list = []
            sleep(0.5)
        print(f"{name} is exiting the main loop")

        while not self.data_queue.empty():
            for i in range(self.batch_vol):
                try:
                    write_list.append(self.data_queue.get_nowait())
                except Empty:
                    break
                except Exception as e:
                    repr(e)
            if len(write_list) > 0:
                # print(f"{name} is inserting")
                self.collection.insert_many(write_list)
                write_list = []
        print(f"{name} exited")

    def simulator(self, name):
        while self.on_going.is_set():
            g, b, s = main.run()
            self.data_queue.put(helplib.get_repr(g, b, s))
            self.simulation_ctr += 1
        print(f"{name} exited")

    def coordinator(self):
        self.on_going.set()
        threads = []
        for i in range(self.simulator_num):
            t = Thread(target=self.simulator, args=(f"Simulator - {i}",))
            t.start()
            threads.append(t)
        print("Simulators booted")
        for i in range(self.db_writer_num):
            w = Thread(target=self.db_writer, args=(f"Db-writer - {i}",))
            w.start()
            threads.append(w)
        print("Db writers booted")
        try:
            while self.on_going.is_set():
                for t in threads:
                    if t.is_alive():
                        print(f"Approx {self.simulation_ctr} items collected, "
                              f"{self.simulation_ctr // (time() - self.simulation_tme)} "
                              f"items per second")
                        sleep(10)
                    else:
                        print("something goes wrong")
                        self.on_going.clear()
        except KeyboardInterrupt as expected:
            self.on_going.clear()
        for t in threads:
            t.join()
        print("The coordinator exited")
        print(f"Approx {self.simulation_ctr} items collected, "
              f"at the speed of {self.simulation_ctr // (time() - self.simulation_tme)} items per second")

    def aggregate(self):
        pass

        # stats = defaultdict(lambda: 0)
        # docs = self.collection.find({}, {"statistics": 1})
        # for doc in docs:
        #     stats[str(len(doc['statistics']))] += 1
        #
        # with open('stats.pickle', 'wb') as handle:
        #     pickle.dump(dict(stats), handle)
        #     print("saved to pickle")

        with open('stats.pickle', 'rb') as handle:
            stats = pickle.load(handle)
        for key in sorted(stats):
            print(key, stats[key])

    def find_ids(self):
        ids_list = []
        docs = self.collection.find({}, {"statistics": 1})
        for doc in docs:
            if len(doc['statistics']) >= 50:
                ids_list.append(doc)
        with open('stats2.pickle', 'wb') as handle:
            pickle.dump(ids_list, handle)

        with open('stats2.pickle', 'rb') as handle:
            ids_list = pickle.load(handle)
        for i, e in enumerate(ids_list):
            print(i, e)

    def db_to_pic(self):  # remember to change the dir and name where the fig store
        with open('stats2.pickle', 'rb') as handle:
            min_list = pickle.load(handle)
        for i in range(0, len(min_list)):
            curr_id = min_list[i]['_id']
            rec = self.collection.find_one({'_id': curr_id})

            # convert to grid object
            new_grid = defaultdict(lambda: [])
            for pos, cars in rec['grid'].items():
                for car in cars:
                    new_grid[tuple(pos)].append({"id": car['id'],
                                                 "when": car['when'],
                                                 "trace": [(e[0], tuple(e[1])) for e in car['trace']]})
            # convert to broadcasters object
            # new_broadcasters = set([tuple(each) for each in rec['broadcasters']])

            # Gui(data=(dict(new_grid), rec['statistics']), mode=1, name=f'PhotoLibrary/fig50/50-{i}-{curr_id}')
            Gui(data=(dict(new_grid), rec['statistics']), mode=0)
            print(i, " finished", len(min_list), "in total")
            break


if __name__ == '__main__':
    worker = Simulation()
    worker.db_to_pic()
    # worker.find_ids()
    # worker.aggregate()
    # worker.coordinator()
