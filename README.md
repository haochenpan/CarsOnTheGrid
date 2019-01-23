# Project Cars On The Grid
#### 1) Branches and explanations:
##### <pre>   dev-1-11-2019 -- prototyping after 01/11/2019 email discussion</pre>
##### <pre>   dev-1-15-2019 -- prototyping after 01/11/2019 email discussion, GUI version 2</pre>
##### <pre>   dev-1-17-2019 (latest) -- confirmed simulation method and GUI after 01/17/2019 office discussion</pre>

#### 2) To install dependent libraries: pip install -r /path/to/requirements.txt

#### 3) Stats of 30000 simulations on 1/21/2019:
##### Config - Row: 20, Col: 20, Num of Cars: 1000 Max round: 100, Allow standing: True
##### X-axis: Number of rounds that used to finish; Y-axis: Number of simulations that used that many rounds
##### All simulations finished in <= 54 rounds, and a few simulations finished in <= 25 rounds.
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/30000.png)
##### A simulation that finished within 25 rounds (~1 percentile of 30000 simulations):
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/fig26/26-10-5c45cfa10871490301fa3903.png)
##### A simulation that finished within 38 rounds (~50 percentile of 30000 simulations):
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/fig38/38-146-5c45cfa10871490301fa397c.png)
##### A simulation that finished within 50 rounds (~99 percentile of 30000 simulations):
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/fig50/50-70-5c45e1940871490218b0bc07.png)
