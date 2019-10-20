from collections import deque
import subprocess as sp
import time, heapq
PATH = "F:\\Root\\ut\\7\\ai\\prj1\\test"
LINK_STATE = {}

class NodeState():
    def __init__(self, location, agent, width):
        self.location = location
        self.price_payed = 0
        self.huristic = 0
        self.agent = agent
        self.width = width
    def manhatan_distante(self, food_location):
        mini = abs(int(food_location[0]/self.width) - int(self.location/self.width)) + abs(int(food_location[0]%self.width - self.location%self.width))
        selected = 0
        for item in food_location:
            curr = abs(int(item / self.width) - int(self.location/self.width)) + abs(int(item % self.width - self.location%self.width))
            if curr < mini:
                mini = curr
                selected = food_location.index(item)
        self.huristic = mini
        return selected, mini
    def add_price(self, delta):
        self.price_payed += delta
    def get_agent(self):
        return self.agent
    def get_location(self):
        return self.location
    def get_price(self):
        return self.price_payed
    def __str__(self):
        return self.price_payed + self.huristic
    def __gt__(self, other):
        if self.price_payed + self.huristic > other.price_payed + other.huristic:
            return True
        else:
            return False
def make_graph_from_file(path_of_file):
    link_state = {}
    p_location = 0
    q_location = 0
    p_foods=[]
    q_foods=[]
    pq_foods=[]
    f = open(path_of_file,"r")
    lines = f.readlines()
    num_of_line = len(lines)
    size_of_line = len(lines[0]) - 1
    for x in range(1,num_of_line - 1):
        for y in range(1,size_of_line - 1):
            if lines[x][y] != '%':
                if lines[x][y] == 'P':
                    p_location = x*size_of_line + y
                if lines[x][y] == 'Q':
                    q_location = x*size_of_line + y
                if lines[x][y] == '1':
                    p_foods.append(x*size_of_line + y)
                if lines[x][y] == '2':
                    q_foods.append(x*size_of_line + y)
                if lines[x][y] == '3':
                    pq_foods.append(x*size_of_line + y)
                neighbor=[]
                if lines[x-1][y] != '%':
                    neighbor.append((x-1)*size_of_line + y)
                if lines[x][y-1] != '%':
                    neighbor.append((x)*size_of_line + y - 1)
                if lines[x+1][y] != '%':
                    neighbor.append((x+1)*size_of_line + y)
                if lines[x][y+1] != '%':
                    neighbor.append((x)*size_of_line + y + 1)
                link_state[x*size_of_line + y]=neighbor
    f.close()
    return link_state, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods
            
def start_bfs(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods):
    queue = deque()
    while len(p_foods + q_foods + pq_foods) != 0:
        print(p_foods, q_foods, pq_foods, p_location, q_location)
        if p_location != 0 and len(p_foods + pq_foods) != 0:
            # print('p')
            queue.append(p_location) 
            p_location = bfs(queue, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods)
        if q_location != 0 and len(q_foods + pq_foods) != 0:
            # print('q')
            queue.append(q_location)
            q_location = bfs(queue, num_of_line, size_of_line, q_location, p_location, q_foods, p_foods, pq_foods)

def bfs(queue, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods):
    pmatrix = [[False for x in range(size_of_line)]for y in range(num_of_line)]   
    pmatrix[int(p_location/size_of_line)][p_location%size_of_line]=True 
    while queue:
        curr = queue.popleft()
        
        # for x in pmatrix:
        #     l = [' 'if y==False else '*' for y in x]
        #     print(l)
        # time.sleep(.05)
        
        # tmp = sp.call('cls',shell=True)
        for nei in LINK_STATE[curr]:
            if nei not in q_foods and nei != q_location and not pmatrix[int(nei/size_of_line)][nei%size_of_line]:
                queue.append(nei)
                pmatrix[int(nei/size_of_line)][nei%size_of_line]=True
            if nei in p_foods:
                p_foods.remove(nei)
                queue.clear()
                return nei
            if nei in pq_foods:
                pq_foods.remove(nei)
                queue.clear()
                return nei
    return p_location

def start_ids(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods):
    max_depgh = (num_of_line-1) * (size_of_line-1)
    for i in range(max_depgh):
        print(i, p_foods, q_foods, pq_foods)
        if len(p_foods) + len(q_foods) + len(pq_foods) == 0:
            break
        if(len(p_foods)+len(pq_foods) != 0):
            ids(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods, i)
        if(len(q_foods)+len(pq_foods) != 0):
            ids(num_of_line, size_of_line, q_location, p_location, q_foods, p_foods, pq_foods, i)
def ids(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods,max_depgh):
    pmatrix = [[0 for x in range(size_of_line)]for y in range(num_of_line)]    
    dfs(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods, 0, max_depgh, pmatrix)
    return
def dfs(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods, depgh, max_depgh, pmatrix):
    if depgh > max_depgh:
        return
    for item in LINK_STATE[p_location]:
        if item not in q_foods and p_location != q_location and pmatrix[int(item/size_of_line)][item%size_of_line]==0:
            pmatrix[int(item/size_of_line)][item%size_of_line]=1
            if item in pq_foods:
                pq_foods.remove(item)
            if item in p_foods:
                p_foods.remove(item)
            dfs(num_of_line, size_of_line, item, q_location, p_foods, q_foods, pq_foods, depgh + 1, max_depgh, pmatrix)
    return 

def start_Astar(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods,pq_foods):
    burder = [NodeState(x,'p',size_of_line) for x in (LINK_STATE[p_location])]
    burder += ([NodeState(x,'q',size_of_line) for x in LINK_STATE[q_location]])
    for item in burder:
        item.add_price(1)
        if(item.get_agent() == 'p'):
            item.manhatan_distante(p_foods + pq_foods)
        else:
            item.manhatan_distante(q_foods + pq_foods)
    heapq.heapify(burder)
    while True:
        curr = heapq.heappop(burder)
        if len(p_foods) + len(q_foods) + len(pq_foods) == 0:
            break

        for item in LINK_STATE[curr.get_location()]:
            if curr.get_agent() == 'p' and len(p_foods) + len(pq_foods) == 0:
                break
            if curr.get_agent() == 'q' and len(q_foods) + len(pq_foods) == 0:
                break
            newitem = NodeState(item, curr.get_agent(), size_of_line)
            newitem.manhatan_distante(p_foods + pq_foods if curr.get_agent() == 'p' else q_foods + pq_foods)
            newitem.add_price(curr.get_price() + 1)
            heapq.heappush(burder, newitem)
            if curr.get_agent() == 'p':
                if item in p_foods:
                    p_foods.remove(item)
                    change_state(burder, LINK_STATE[curr.get_location()], LINK_STATE[q_location],size_of_line)
                    break
                elif item in pq_foods:
                    pq_foods.remove(item)
                    change_state(burder, LINK_STATE[curr.get_location()], LINK_STATE[q_location],size_of_line)
                    break
            else:
                if item in q_foods:
                    q_foods.remove(item)
                    change_state(burder, LINK_STATE[p_location], LINK_STATE[curr.get_location()],size_of_line)
                    break
                elif item in pq_foods:
                    pq_foods.remove(item)
                    change_state(burder, LINK_STATE[p_location], LINK_STATE[curr.get_location()],size_of_line)
                    break
    return 
def change_state(heap, p_nei, q_nei, size_of_line):
    heap = []
    for item in p_nei:
        newitem = NodeState(item, 'p', size_of_line)
        newitem.add_price(1)
        heap.append(newitem)
    for item in q_nei:
        newitem = NodeState(item, 'q', size_of_line)
        newitem.add_price(1)
        heap.append(newitem)
    heapq.heapify(heap)
    return heap

for i in range(1,6):
    link_state, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods= make_graph_from_file(PATH+str(i))
    LINK_STATE = link_state.copy()
    start_bfs(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods,pq_foods)
    # start_ids(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods)
    # start_Astar(num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods)
    print(p_foods, q_foods, pq_foods)