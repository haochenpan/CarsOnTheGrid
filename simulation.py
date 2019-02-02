"""
    Multi-threading simulation doesn't increase the speed,
    open several terminals and do multi-processing instead (for now)
"""
from collections import defaultdict
from threading import Thread, Event
from time import sleep, time
from queue import Empty, Queue
from pymongo import MongoClient
import pickle
import main
from gui import Gui
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self):
        self.on_going = Event()
        self.data_queue = Queue()
        self.batch_vol = 50
        self.simulator_num = 1
        self.db_writer_num = 1
        self.simulation_ctr = 0  # a approx counter due to race condition
        self.simulation_tme = time()
        self.collection = MongoClient()['CarsOnTheGrid']['r20c20n1000r100-0201']

    def _db_writer(self, name):
        write_list = []
        while self.on_going.is_set():
            approx_qsize = self.data_queue.qsize()
            # print(f"{name} says approx_qsize is", approx_qsize)
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
        # print(f"{name} is exiting the main loop")

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
        # print(f"{name} exited")

    def _simulator(self, name):
        while self.on_going.is_set():
            g, s = main.run()
            self.data_queue.put(s)
            self.simulation_ctr += 1
        # print(f"{name} exited")

    def coordinate(self):
        self.on_going.set()
        threads = []
        for i in range(self.simulator_num):
            t = Thread(target=self._simulator, args=(f"Simulator - {i}",))
            t.start()
            threads.append(t)
        print("Simulators booted")
        for i in range(self.db_writer_num):
            w = Thread(target=self._db_writer, args=(f"Db-writer - {i}",))
            w.start()
            threads.append(w)
        print("Db writers booted")
        try:
            while self.on_going.is_set():
                for t in threads:
                    if t.is_alive():
                        print(f"Approx {self.simulation_ctr} items collected, "
                              f"{self.simulation_ctr // (time() - self.simulation_tme)} items per second"
                              f"data_queue size: {self.data_queue.qsize()}")
                        sleep(5)
                    else:
                        print("something goes wrong")
                        self.on_going.clear()
        except KeyboardInterrupt as expected:
            self.on_going.clear()
        for t in threads:
            t.join()
        print("The coordinate exited")
        print(f"Approx {self.simulation_ctr} items collected, "
              f"at the speed of {self.simulation_ctr // (time() - self.simulation_tme)} items per second")

    def aggregate(self, filename):
        """
        aggregate to generate the bell curve
        :return:
        """

        # aggregate from the db
        # stats = defaultdict(lambda: 0)
        # docs = self.collection.find({}, {"stats": 1})
        # for doc in docs:
        #     stats[str(len(doc['stats']))] += 1
        #
        # with open('stats.pickle', 'wb') as handle:
        #     pickle.dump(dict(stats), handle)
        #     print("saved to pickle")
        #

        # print aggregate dict
        # with open('stats.pickle', 'rb') as handle:
        #     stats = pickle.load(handle)
        # for key in sorted(stats):
        #     print(key, stats[key])

        # plot aggregate dict
        fig, ax = plt.subplots(figsize=(12, 12))
        with open('stats.pickle', 'rb') as handle:
            stats = pickle.load(handle)
        x, y = [], []
        for key in sorted(stats):
            x.append(key)
            y.append(stats[key])
        ax.scatter(x, y, alpha=0.8)

        for i, d in enumerate(y):
            ax.annotate(d, (x[i], y[i]), size=8)
        plt.savefig(f'{filename}.png')

    def find_ids(self):
        ids_list = []
        docs = self.collection.find({}, {"stats": 1})
        for doc in docs:
            if len(doc['stats']) <= 25:
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
            record = self.collection.find_one({'_id': curr_id})
            stats = {
                "stats": [tuple(each) for each in record['stats']],
                "trace": [(each[0], tuple(each[1])) for each in record['trace']],
                "confi": record['confi']
            }
            # convert to grid object
            # new_grid = defaultdict(lambda: [])
            # for pos, cars in record['grid'].items():
            #     for car in cars:
            #         new_grid[tuple(pos)].append({"id": car['id'],
            #                                      "when": car['when'],
            #                                      "trace": [(e[0], tuple(e[1])) for e in car['trace']]})
            # convert to broadcasters object
            # new_broadcasters = set([tuple(each) for each in rec['broadcasters']])

            Gui(data=(None, stats), mode=1, path=f'PhotoLibrary/Feb-50000/fig25/25-{i}-{curr_id}')
            # Gui(data=(None, stats), mode=0)
            print(i, " finished", len(min_list), "in total")


if __name__ == '__main__':
    worker = Simulation()
    # worker.coordinate()
    # worker.aggregate("50000")
    worker.find_ids()
    worker.db_to_pic()
