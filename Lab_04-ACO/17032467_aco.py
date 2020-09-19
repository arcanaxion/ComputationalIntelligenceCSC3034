### THIS 

from itertools import accumulate
import random
import matplotlib.pyplot as plt

location_list = [ # [x,y,name]
  [75, 125, 'Arad'],
  [100, 75, 'Zerind'],
  [125, 25, 'Oradea'],
  [265, 175, 'Sibiu'],
  [425, 175, 'Fagaras'],
  [320, 230, 'Rimnicu Vilcea'],
  [475, 310, 'Pitesti'],
  [350, 465, 'Craiova'],
  [185, 450, 'Drobeta'],
  [190, 390, 'Mehadia'],
  [185, 335, 'Lugoj'],
  [85, 280, 'Timisoara'],
  [640, 390, 'Bucharest'],
  [575, 485, 'Giurgiu'],
  [745, 340, 'Urziceni'],
  [875, 340, 'Hirsova'],
  [935, 440, 'Eforie'],
  [850, 225, 'Vaslui'],
  [760, 120, 'Iasi'],
  [625, 60, 'Neamt']
]

step_cost = [
  ['Arad', 'Zerind', 75],
  ['Zerind', 'Oradea', 71],
  ['Oradea', 'Sibiu', 151],
  ['Sibiu', 'Arad', 140],
  ['Sibiu', 'Fagaras', 99],
  ['Sibiu', 'Rimnicu Vilcea', 80],
  ['Fagaras', 'Bucharest', 211],
  ['Bucharest', 'Giurgiu', 90],
  ['Bucharest', 'Pitesti', 101],
  ['Pitesti', 'Rimnicu Vilcea', 97],
  ['Rimnicu Vilcea', 'Craiova', 146],
  ['Craiova', 'Pitesti', 138],
  ['Craiova', 'Drobeta', 120],
  ['Drobeta', 'Mehadia', 75],
  ['Mehadia', 'Lugoj', 70],
  ['Lugoj', 'Timisoara', 111],
  ['Arad', 'Timisoara', 118],
  ['Bucharest', 'Urziceni', 85],
  ['Urziceni', 'Vaslui', 142],
  ['Vaslui', 'Iasi', 92],
  ['Iasi', 'Neamt', 87],
  ['Urziceni', 'Hirsova', 98],
  ['Hirsova', 'Eforie', 86]
]

def create_graph(cities):
  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)
  cities_x = [city.coordinates[0] for key, city in cities.items()]
  cities_y = [city.coordinates[1] for key, city in cities.items()]
  ax.scatter(cities_x, cities_y)
  ax.set_aspect(aspect=1.0)
  return ax

def draw_pheromone(ax, roads):
  lines = []
  for road in roads:
    from_coord = road.connected_cities[0].coordinates
    to_coord = road.connected_cities[1].coordinates
    coord_x = [from_coord[0], to_coord[0]]
    coord_y = [from_coord[1], to_coord[1]]
    lines.append(ax.plot(coord_x, coord_y, c='k', linewidth=road.pheromone**2))
  return lines

class City:
  def __init__(self, name):
    self.name = name
    self.roads = []
    self.coordinates = []
    
  def set_coordinates(self, coordinates):
    self.coordinates = coordinates

  def add_road(self, road):
    if road not in self.roads:
      self.roads.append(road)

class Road:
  def __init__(self, connected_cities, cost, pheromone=0):
    self.connected_cities = connected_cities
    self.cost = cost
    self.pheromone = pheromone
  def set_pheromone(self, pheromone):
    self.pheromone = pheromone
  def evaporate_pheromone(self, rho):
    # update the pheromone of the road
    self.pheromone *= (1-rho)
  def deposit_pheromone(self, ants):
    # 1. search for ants that uses the raod
    using_ants = []
    for ant in ants:
      if self in ant.path:
        using_ants.append(ant)
    # 2. deposit pheromone using the inversely proportionate relationship 
    # between path length and deposited pheromone
    to_deposit = sum([1/ant.get_path_length() for ant in using_ants])
    self.pheromone += to_deposit

class Ant:
  def __init__(self):
    self.cities = [] # cities the ant passes through, in sequence
    self.path = [] # roads the ant uses, in sequence
  def get_path(self, origin, destination, alpha):
    # 1. append origin to the self.cities
    self.cities.append(origin)
    # 2. if the last city is not destination, search for the next city to go
    latest_city = self.cities[-1]
    while latest_city != destination:
      connected_roads = latest_city.roads
      pm_sum_with_alpha = sum([alpha * road.pheromone for road in connected_roads])
      probability_list = [(alpha * road.pheromone) / pm_sum_with_alpha for road in connected_roads]
      selected_road = random.choices(population=connected_roads, weights=probability_list)[0]
      if selected_road.connected_cities[0] == latest_city:
        latest_city = selected_road.connected_cities[1]
      else:
        latest_city = selected_road.connected_cities[0]
      self.cities.append(latest_city)
      self.path.append(selected_road)
    # 3. after getting to the destination, remove the loop within the path, 
    # i.e. if there are repeated cities in self.cities, remove the cities and the 
    # roads in between the repetition
    while len(set(self.cities)) != len(self.cities):
      loop = True
      for start_ind, a_city in enumerate(self.cities):
        for end_ind, b_city in enumerate(self.cities):
          if start_ind != end_ind and a_city == b_city:
            loop = False
            for _ in range(start_ind, end_ind):
              del self.cities[start_ind]
              del self.path[start_ind]
          if not loop:
            break
        if not loop:
          break

  def get_path_length(self):
    # calculate path length based on self.path
    path_length = 0
    for each in self.path:
      path_length += each.cost
    return path_length
  def reset(self):
    self.path = []
    self.cities = []

def most_common(lst):
  freq = [] # (elem, frequency)
  for i in lst:
    count = 0
    for y in lst:
      if i == y:
        count += 1
    freq.append((i, count))
  return max(freq, key=lambda x: x[1])[0]

def get_percentage_of_dominant_path(ants):
  paths = [ant.path for ant in ants]
  if not paths[0]:
    return 0.1
  return paths.count(most_common(paths)) / len(ants)

if __name__ == "__main__":
  cities = {}
  for coord1, coord2, name in location_list:
    cities[name] = City(name)
    cities[name].set_coordinates([coord1, coord2])
  roads = []
  for city1, city2, cost in step_cost:
    road = Road([cities[city1], cities[city2]], cost)
    cities[city1].add_road(road)
    cities[city2].add_road(road)
    roads.append(road)

  origin = cities['Arad']
  destination = cities['Bucharest']

  n_ant = 100
  alpha = 1
  rho = 0.1

  initial_pheromone = 0.01
  for road in roads:
    road.set_pheromone(initial_pheromone)

  ants = [Ant() for _ in range(n_ant)]

  # termination threshold
  max_iteration = 200
  percentage_of_dominant_path = 0.9

  ax = create_graph(cities)
  lines = draw_pheromone(ax, roads)

  iteration = 0
  while get_percentage_of_dominant_path(ants) < percentage_of_dominant_path and iteration < max_iteration: # termination conditions
    print("Iteration: {0}\tPercentage: {1}".format(iteration, get_percentage_of_dominant_path(ants)))
    # loop through all the ants to identify the path of each ant
    for ant in ants:
      # reset the path of the ant
      ant.reset()
      # identify the path of the ant
      ant.get_path(origin, destination, alpha)
    # loop through all roads
    for road in roads:
      # evaporate the pheromone on the road
      road.evaporate_pheromone(rho)
      # deposit the pheromone
      road.deposit_pheromone(ants)
    # increase iteration count
    iteration += 1
    # visualise
    for l in lines:
      del l
    lines = draw_pheromone(ax, roads)
    plt.pause(0.05)
  # after exiting the loop, return the most occurred path as the solution
  # for road in roads:
  #   print("Road cost: {}\tPheromone: {:.2f}".format(road.cost, road.pheromone))
  print(["{}-{}".format(pt.connected_cities[0].name, 
  pt.connected_cities[1].name) for pt in most_common([ant.path for ant in ants])])
  plt.show()