from collections import deque

PATH = "F:\\Root\\ut\\7\\ai\\prj1\\test1"

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
    size_of_line = len(lines[0])
    for x in range(1,num_of_line - 1):
        for y in range(1,size_of_line - 1):
            if lines[x][y] != '%':
                if lines[x][y] == 'P':
                    p_location = x*num_of_line + y
                if lines[x][y] == 'Q':
                    q_location = x*num_of_line + y
                if lines[x][y] == '1':
                    p_foods.append(x*num_of_line + y)
                if lines[x][y] == '2':
                    q_foods.append(x*num_of_line + y)
                if lines[x][y] == '3':
                    pq_foods.append(x*num_of_line + y)
                neighbor=[]
                if lines[x-1][y] != '%':
                    neighbor.append((x-1)*num_of_line + y)
                if lines[x][y-1] != '%':
                    neighbor.append((x)*num_of_line + y - 1)
                if lines[x+1][y] != '%':
                    neighbor.append((x+1)*num_of_line + y)
                if lines[x][y+1] != '%':
                    neighbor.append((x)*num_of_line + y + 1)
                link_state[x*num_of_line + y]=neighbor
    f.close()
    return link_state, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods
            
def start_bfs(link_state, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods):
    queue = deque()
    queue.append(p_location) 
    bfs(queue, link_state, num_of_line, size_of_line, p_location, p_foods, q_foods, pq_foods)
    queue.append(q_location)
    bfs(queue, link_state, num_of_line, size_of_line, q_location, q_foods, p_foods, pq_foods)

def bfs(queue, link_state, num_of_line, size_of_line, p_location, p_foods, q_foods, pq_foods):
    pmatrix = [[False for x in range(size_of_line)]for y in range(num_of_line)]    
    while queue:
        curr = queue.popleft()
        for nei in link_state[curr]:
            if nei not in q_foods and nei != q_location and not pmatrix[int(nei/num_of_line)][nei%num_of_line]:
                queue.append(nei)
                pmatrix[int(nei/num_of_line)][nei%num_of_line]=True
            if nei in p_foods:
                p_foods.remove(nei)
            if nei in pq_foods:
                pq_foods.remove(nei)
    return 

                           
link_state, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods, pq_foods= make_graph_from_file(PATH)

start_bfs(link_state, num_of_line, size_of_line, p_location, q_location, p_foods, q_foods,pq_foods)