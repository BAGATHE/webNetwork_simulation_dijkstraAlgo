from collections import deque

class Server:
    def __init__(self, ip):
        self._ip = ip
        self._ipId =None
        self._distance = float('inf')
        self._predecessor = None
        self._neighbors = []
        self._points = []
        self._hostedSiteList = []
        self._image = None
        self._idImage = None
        self._line = []
        self._refping = []
        self._linePath=[]
        self._isAvailable=None

    def get_ip(self):
        return self._ip

    def set_ip(self, value):
        self._ip = value
    
    def get_ipId(self):
        return self._ipId

    def set_ipId(self, value):
        self._ipId = value

    def get_distance(self):
        return self._distance

    def set_distance(self, value):
        self._distance = value

    def get_predecessor(self):
        return self._predecessor

    def set_predecessor(self, value):
        self._predecessor = value

    def get_neighbors(self):
        return self._neighbors

    def add_neighbor(self, neighbor, ping):
        self._neighbors.append([neighbor, ping])

    def get_points(self):
        return self._points

    def set_points(self, value):
        self._points = value

    def get_hostedSiteList(self):
        return self._hostedSiteList
    
    def add_hostedSiteList(self,value):
        self._hostedSiteList.append(value)

    def set_hostedSiteList(self, value):
        self._hostedSiteList = value
    
    def get_image(self):
        return self._image

    def set_image(self, value):
        self._image = value
    
    def get_idImage(self):
        return self._idImage

    def set_idImage(self, value):
        self._idImage = value
        
    def get_line(self):
        return self._line

    def set_line(self, value):
        self._line = value

    def get_linePath(self):
        return self._line

    def set_linePath(self, value):
        self._line = value
    
    def get_refping(self):
        return self._refping

    def set_refping(self, value):
        self._refping = value
    
    def add_refping(self,value):
        self._refping.append(value)
    
    def get_isAvailable(self):
        return self._isAvailable
    def set_isAvailable(self,value):
        self._isAvailable = value

    def get_Server_by_ip(ip_address,tab_Servers):
        for server in tab_Servers:
            if server.get_ip() == ip_address:
                return server
    
    def containsSite(self,site):
        if site in self.get_hostedSiteList():
            return True
        else:
            return False


    def find_servers_hosting_site(serverSource,url,tab_servers):
        found_servers = []
        if url in serverSource.get_hostedSiteList():
            found_servers.append(serverSource)
            return found_servers
        for server in tab_servers:
            if url in server.get_hostedSiteList():
                found_servers.append(server)
        return found_servers
    
    def sumPing(self):
        sum = 0
        for neighbor in self.get_neighbors():
            sum += neighbor[1]
        return sum
    
    def clear_lines(self, canvas):
        for line_id in self.get_linePath():
            canvas.delete(line_id)
        self._linePath=[]   

def extract_min(unvisitedServer):
        min_distance = float('inf')
        min_server = None
        for server in unvisitedServer:
            if server.get_distance() < min_distance:
                min_distance = server.get_distance()
                min_server = server
        unvisitedServer.remove(min_server)
        return min_server
 
    
    
def dijkstra_shortest_path(servers, serverSource, destination):
    for server in servers:
        if server.get_ip()==serverSource.get_ip():
            server.set_distance(0)
            server.set_predecessor(None)
        else:  
            server.set_distance(float('inf'))
            server.set_predecessor(None)
    
    visited = set()
    unvisited = set(servers)
    while unvisited:
        current_server = extract_min(unvisited)
        visited.add(current_server)
        for neighbor, ping in current_server.get_neighbors():
            if neighbor not in visited:
                ping = int(ping)
                if neighbor.get_distance() > current_server.get_distance() + ping:
                    neighbor.set_distance(current_server.get_distance() + ping)
                    neighbor.set_predecessor(current_server)
                   
    shortest_path = []
    current = destination
    while current is not None:
        shortest_path.insert(0, current)
        current = current.get_predecessor()
    distance = destination.get_distance()
    return shortest_path,distance
      
    

def BFS(start, site):
    file = []
    start.set_isAvailable(False)
    enfiler(file, start)
    trajectory = []
    if start.containsSite(site):
        return [start]
    
    while file:
        last = defiler(file)
        for neighbor,ping in last.get_neighbors():
            u = neighbor
            if u.isAvailable:
                u.setParent(last)
                u.setIsAvailable(False)
                enfiler(file, u)
                if u.containsSite(site):
                    while u:
                        trajectory.append(u)
                        u = u.getParent()
                    return trajectory[::-1]
        return trajectory

def enfiler(file, node):
    file.append(node)

def defiler(file):
    node = file.pop()
    return node

    
