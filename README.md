# Project Cars On The Grid
## More precisely, the project name is "Cars In Blocks"
#### 1) To install dependent libraries:
`pip install -r /path/to/requirements.txt` 

#### 2) Program Structure (for collaborators)

##### Read this first:
###### config.py

##### Simulation:
###### main.py (all lines)
###### helplib.py (all lines before the comment 'GUI Helper Library')
###### test.py (all test cases... for now)

##### Visualization (GUI):
###### all remaining code

#### 3) Stats of 30000 simulations on 1/21/2019:
##### Config - Row: 20, Col: 20, Num of Cars: 1000 Max round: 100, Allow standing: True
##### X-axis: Number of rounds that used to finish; Y-axis: Number of simulations that used that many rounds
##### All simulations finished in <= 54 rounds, and a few simulations finished in <= 25 rounds.
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/30000.png)

##### Typical simulation that finished within 25 rounds (~1 percentile of 30000 simulations):
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/fig26/26-12-5c45cfa10871490301fa3a77.png)
##### Typical simulation that finished within 38 rounds (~50 percentile of 30000 simulations):
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/fig38/38-17-5c45cd8d08714902ba773e8c.png)
##### Typical simulation that finished within 50 rounds (~99 percentile of 30000 simulations):
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-1-17-2019/PhotoLibrary/fig50/50-19-5c45d2e1087149037e37ff65.png)


