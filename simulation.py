"""
    Generate during simulation:
        Grid object, Broadcaster object, Stats, Config Snapshot
    Generate during GUI call:
        Grid object -> Plotting positions (for the first round)
        Plotting positions -> Line spaces (for all animations)
        Grid object -> Colors (for all rounds)
        Grid object -> Source's positions on the second graph
"""

from threading import Thread, Event
from time import sleep, time
from queue import Empty, Queue
from pymongo import MongoClient
import main
import helplib


class Simulation:
    def __init__(self):
        self.on_going = Event()
        self.data_queue = Queue()
        self.batch_vol = 100
        self.simulator_num = 60
        self.db_writer_num = 20
        self.simulation_ctr = 0  # a approx counter due to race condition
        self.simulation_tme = time()
        self.collection = MongoClient()['CarsOnTheGrid']['r20c20n1000r10']

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
                print(f"{name} is inserting")
                self.collection.insert_many(write_list)
                write_list = []
            sleep(3)
        print(f"{name} is exiting the main loop")

        while not self.data_queue.empty():
            try:
                write_list.append(self.data_queue.get_nowait())
            except Empty:
                break
            except Exception as e:
                repr(e)
        if len(write_list) > 0:
            self.collection.insert_many(write_list)
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
                        print("writer is alive!")
                        sleep(10)
                    else:
                        print("something goes wrong")
                        self.on_going.clear()
        except KeyboardInterrupt as expected:
            self.on_going.clear()
        for t in threads:
            t.join()
        print("coordinator exited")
        print(f"Approx {self.simulation_ctr} items collected, "
              f"at the speed of {self.simulation_ctr // (time() - self.simulation_tme)} items per second")


if __name__ == '__main__':
    worker = Simulation()
    worker.coordinator()
