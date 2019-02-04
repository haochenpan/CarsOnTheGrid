# Project Cars On The Grid
## More precisely, the project name is "Cars In Blocks"
#### 1) To install dependent libraries:
`pip install -r /path/to/requirements.txt` 

#### 2) Program Structure (for collaborators)

###### Read this first:
###### `config.py`

###### Simulation:
###### `main.py` (all lines)
###### `helplib.py` (all lines before the comment 'GUI Helper Library')
###### `test.py` (all test cases... for now)

###### Visualization (GUI):
###### all remaining code

#### 3) Findings from 50000+ simulations on Feb

##### Good old distribution -- x-axis: rounds need to finish simulation; y-axis: the number of rounds
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-2-2-2019/50000.png)
##### Distribution -- average span(area) of the source
##### Interpretation -- Ignoring extremes points (due to lack of data), we see a trival fact that more rounds need to finish a simulation implies bigger the source's span/area moves. Thus, how many rounds the source needs to let every car hear the message has little to do with the area of the span(?).
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-2-2-2019/round-area.png)
##### Distribution -- average center of the span(area) of the source
##### Interpretation -- We see another trival fact that the average center of the span area is likely to be the center of the grid because simulations that need a certain # of rounds to finish balanced their average data (e.g. 1000 cases have their centers at the top of the graph and 1000 cases have their centers at the bottom of the graph, thus they balance the overall average to the center of the grid)
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-2-2-2019/round-xy.png)
##### Distribution -- average difference from the average of 4 spaces by rounds finished (The title is confusing, I will come up a better one)
##### Interpretation -- The intuition is that if the source is closer to the center, the faster the message broadcasts. Here's how I naively quantify this: For each simulation, I first measured the rectangular space of the source's span on the grid, and calculated 4 distances, each distance is from a broader of the grid to the closest broader of the rectangular space. The averages of the sum of the 4 distances(I label them as spaces on the figure) by rounds need to finish a simulation are blue dots. Then I calculated corresponding 4 differences, each difference = abs(distance - avg), and added them together, that are yellow dots.
![](https://github.com/haochenpan/CarsOnTheGrid/blob/dev-2-2-2019/round-diff.png)
