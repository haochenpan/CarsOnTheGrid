"""
    Simulation: Simulate the game multiple times, store results to DB
    Statistics: Query the DB to produce statistical results

    Python's multi-threading DECREASES the speed,
    so open several terminals to do multi-processing instead (for now)
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
from pprint import PrettyPrinter

COLLECTION_NAME = 'r20c20n1000r100-0205'


class Simulation:
    def __init__(self):
        self.on_going = Event()  # records user keyboard interruption
        self.batch_vol = 50  # the number of records involves in a DB batch write
        self.data_queue = Queue()
        self.simulator_num = 1
        self.db_writer_num = 1
        self.simulation_ctr = 0  # a approximate counter of records (due to race condition)
        self.simulation_tme = time()  # the start time
        self.collection = MongoClient()['CarsOnTheGrid'][COLLECTION_NAME]

    def _db_writer(self, name):
        write_list = []
        # while the keyboard interruption has not been trigger OR
        # there's some data that have not stored to DB:
        while self.on_going.is_set() or not self.data_queue.empty():
            approx_qsize = self.data_queue.qsize()
            # print(f"{name} says approx_qsize is", approx_qsize)
            for i in range(self.batch_vol):
                try:
                    write_list.append(self.data_queue.get_nowait())
                except Empty:
                    break
            if len(write_list) > 0:
                self.collection.insert_many(write_list)
                write_list = []
            sleep(0.5)

        print(f"{name} exited")

    def _simulator(self, name):
        while self.on_going.is_set():
            g, s = main.run()
            self.data_queue.put(s)  # can adjust whether the simulator stores the grid or not
            self.simulation_ctr += 1
        print(f"{name} exited")

    def coordinate(self):
        # the parent program initiates two kinds of threads
        self.on_going.set()
        threads = []
        for i in range(self.simulator_num):
            t = Thread(target=self._simulator, args=(f"Simulator - {i}",))
            t.start()
            threads.append(t)
        print("Simulator(s) booted")
        for i in range(self.db_writer_num):
            w = Thread(target=self._db_writer, args=(f"Db-writer - {i}",))
            w.start()
            threads.append(w)
        print("DB writer(s) booted")

        # the parent program check threads' heartbeat and user's keyboard interruption
        try:
            while self.on_going.is_set():
                items_per_second = self.simulation_ctr // (time() - self.simulation_tme)
                print(f"Approx {self.simulation_ctr} items collected, "
                      f"{items_per_second} items per second, "
                      f"approx data_queue size: {self.data_queue.qsize()}")
                sleep(5)
        except KeyboardInterrupt as expected:
            self.on_going.clear()
        finally:
            for t in threads:
                t.join()
        print("The coordinate exited")
        print(f"Approx {self.simulation_ctr} items collected, "
              f"at the speed of {self.simulation_ctr // (time() - self.simulation_tme)} items per second")


class Statistics:
    def __init__(self):
        self.collection = MongoClient()['CarsOnTheGrid'][COLLECTION_NAME]

    def aggregate(self, filename):
        """
        aggregate to generate the bell curve
        :return:
        """

        # aggregate from the db
        stats = defaultdict(lambda: 0)
        docs = self.collection.find({}, {"stats": 1})
        for doc in docs:
            stats[str(len(doc['stats']))] += 1

        with open('stats.pickle', 'wb') as handle:
            pickle.dump(dict(stats), handle)
            print("saved to pickle")


        # print aggregate dict
        with open('stats.pickle', 'rb') as handle:
            stats = pickle.load(handle)
        for key in sorted(stats):
            print(key, stats[key])

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

    @staticmethod
    def record_to_pic(record):
        stats = {
            "stats": [tuple(each) for each in record['stats']],
            "trace": [(each[0], tuple(each[1])) for each in record['trace']],
            "confi": record['confi']
        }

        # Gui(data=(None, stats), mode=1, path=f'PhotoLibrary/Feb-50000/fig25/25-{i}-{curr_id}')
        Gui(data=(None, stats), mode=1)

        # print(i, " finished", len(min_list), "in total")

    @staticmethod
    def record_to_sta(self, record):
        h_min, h_max = record['confi']['LAST_COL_INDEX'], record['confi']['FIRST_COL_INDEX']
        v_min, v_max = record['confi']['LAST_ROW_INDEX'], record['confi']['FIRST_ROW_INDEX']
        for dir_and_pos in record['trace']:
            pos_r = dir_and_pos[1][0]
            pos_c = dir_and_pos[1][1]
            h_min = pos_c if pos_c < h_min else h_min
            h_max = pos_c if pos_c > h_max else h_max
            v_min = pos_r if pos_r < v_min else v_min
            v_max = pos_r if pos_r > v_max else v_max

        # print(h_min, h_max)
        # print(v_min, v_max)

        source_span_area = (h_max - h_min + 1) * (v_max - v_min + 1)
        source_span_ctr_x = (h_max + h_min) / 2  # float is desirable
        source_span_ctr_y = (v_max + v_min) / 2
        source_span_ctr = source_span_ctr_x, source_span_ctr_y
        # print("source_span_area", source_span_area)
        # print("source_span_ctr", source_span_ctr)

        v_direction_tail = record['trace'][0][1]
        v_direction_head = record['trace'][-1][1]
        vector_direction = (v_direction_head[0] - v_direction_tail[0],
                            v_direction_head[1] - v_direction_tail[1],)
        # print(v_direction_head, v_direction_tail, vector_direction)
        return {
            "h_min": h_min,
            "h_max": h_max,
            "v_min": v_min,
            "v_max": v_max,
            "source_span_area": source_span_area,
            "source_span_ctr": source_span_ctr,
            "vector_direction": vector_direction
        }

    def summarize_record(self):
        recs = self.collection.find().skip(1000)
        for rec in recs:
            # self.record_to_pic(rec)
            stat = self.record_to_sta(rec)
            self.collection.update_one({'_id': rec['_id']}, {'$set': {'summary': stat}})

        # pp = PrettyPrinter()
        # pp.pprint(rec['trace'])
        # pp.pprint(rec['confi'])

    def find_relation1(self):
        # collect from db - area
        st = defaultdict(lambda: [0, 0])
        docs = self.collection.find({}, {"stats": 1, "summary": 1})
        for doc in docs:
            st[str(len(doc['stats']))][0] += 1
            st[str(len(doc['stats']))][1] += doc['summary']['source_span_area']

        # # collect from db - xy
        # st = defaultdict(lambda: [0, 0, 0])
        # docs = self.collection.find({}, {"stats": 1, "summary": 1})
        # for doc in docs:
        #     st[str(len(doc['stats']))][0] += 1
        #     st[str(len(doc['stats']))][1] += doc['summary']['source_span_ctr'][0]
        #     st[str(len(doc['stats']))][2] += doc['summary']['source_span_ctr'][1]

        # store to pickle - shared
        with open('stats.pickle', 'wb') as handle:
            pickle.dump(dict(st), handle)
            print("saved to pickle")

        with open('stats.pickle', 'rb') as handle:
            st = pickle.load(handle)

        # print result - area
        for key in sorted(st):
            print(key, "area_avg", st[key][1] // st[key][0])

        # print result - xy
        # for key in sorted(st):
        #     print(key, "h_avg", round(st[key][1]/st[key][0], 2), "v_avg", round(st[key][2]/st[key][0], 2))

        # composition 1 - shared
        fig, ax = plt.subplots(figsize=(15, 15))
        x, y, z = [], [], []

        # load data - area
        for key in sorted(st):
            x.append(key)
            y.append(st[key][1] // st[key][0])
        ax.scatter(x, y, alpha=0.8, label='area_avg')

        # load data - xy
        # for key in sorted(st):
        #     x.append(key)
        #     y.append(round(st[key][1]/st[key][0], 1))
        #     z.append(round(st[key][2]/st[key][0], 1))
        # ax.scatter(x, y, alpha=0.8, label='col_avg')  # h_avg = col_avg
        # ax.scatter(x, z, alpha=0.8, label='row_avg')

        # composition 2 - area
        for i, d in enumerate(y):
            ax.annotate(d, (x[i], y[i] + 0.25), size=8)
        plt.legend(loc='upper left')
        plt.xlabel('Rounds Need to Finish')
        plt.ylabel('Average Area (Sqrt Block)')
        plt.title('Averages Area of the Source\'s Span Area by Rounds Finished')
        plt.savefig(f'{"round-area"}.png')

        # composition 2 - xy
        # for i, d in enumerate(y):
        #     ax.annotate(d, (x[i], y[i] + 0.5), size=8)
        #     ax.annotate(z[i], (x[i], z[i] - 0.5), size=8)
        # plt.legend(loc='upper left')
        # plt.xlabel('Rounds Need to Finish')
        # plt.ylabel('Average Row/Col (to 1 decimal place)')
        # plt.title('Averages Row and Col of the Center of the Source\'s Span Area by Rounds Finished')
        # plt.savefig(f'{"round-xy"}.png')

    def find_relation2(self):
        st = defaultdict(lambda: [0, 0, 0, 0])
        docs = self.collection.find({}, {"confi": 1, "stats": 1, "trace": 1, "summary": 1})
        for doc in docs:
            # self.record_to_pic(doc)
            rd = len(doc['stats'])

            h_min_space = doc['summary']['h_min'] - doc['confi']['FIRST_ROW_INDEX']
            h_max_space = doc['confi']['LAST_ROW_INDEX'] - doc['summary']['h_max'] + 1
            v_min_space = doc['summary']['v_min'] - doc['confi']['FIRST_ROW_INDEX']
            v_max_space = doc['confi']['LAST_COL_INDEX'] - doc['summary']['v_max'] + 1
            assert h_min_space >= 0
            assert h_max_space >= 0
            assert v_min_space >= 0
            assert v_max_space >= 0
            # print(doc['summary']['h_min'], doc['summary']['h_max'],
            #       doc['summary']['v_min'], doc['summary']['v_max'])
            # print(h_min_space, h_max_space, v_min_space, v_max_space)
            avg = (h_min_space + h_max_space + v_min_space + v_max_space) / 4
            dif = abs(h_min_space - avg) + abs(h_max_space - avg) + abs(v_min_space - avg) + abs(v_max_space - avg)
            # print(avg, dif)
            st[rd][0] += 1
            st[rd][1] += avg
            st[rd][2] += dif

        # with open('stats.pickle', 'wb') as handle:
        #     pickle.dump(dict(st), handle)
        #     print("saved to pickle")

        # with open('stats.pickle', 'rb') as handle:
        #     st = pickle.load(handle)
        for key in sorted(st):
            print(key, "avg_avg", st[key][1] // st[key][0], "avg_dif", st[key][2] // st[key][0])

        fig, ax = plt.subplots(figsize=(12, 12))
        x, y, z = [], [], []

        for key in sorted(st):
            x.append(key)
            y.append(st[key][1] // st[key][0])
            z.append(st[key][2] // st[key][0])
        ax.scatter(x, y, alpha=0.8, label='the_average_of_4_spaces')  # h_avg = col_avg
        ax.scatter(x, z, alpha=0.8, label='the_sum_of_4_differences_from_the_avg')

        for i, d in enumerate(z):
            ax.annotate(y[i], (x[i], y[i] + 0.5), size=8)
            ax.annotate(d, (x[i], z[i] - 0.5), size=8)
        plt.legend(loc='upper left')
        plt.xlabel('Rounds Need to Finish')
        plt.ylabel('Row/Col')
        plt.title('Averages Difference by Rounds Finished')
        plt.savefig(f'{"round-diff"}.png')


if __name__ == '__main__':
    pass
    # worker = Simulation()
    # worker.coordinate()
    # worker.aggregate("50000")
    # worker.find_ids()
    # worker.db_to_pic()
    # stats = Statistics()
    # stats.summarize_record()
    # stats.find_relation2()
