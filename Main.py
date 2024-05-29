from CustomFrame import CustomFrame
from Server import Server
from Server import dijkstra_shortest_path
from Server import BFS

if __name__ == "__main__":
    root = CustomFrame()
    root.mainloop()
    server_A = Server("A")
    server_B = Server("B")
    server_C = Server("C")
    server_D = Server("D")
    server_E = Server("E")

# Ajout des voisins avec leurs ping respectifs
    server_A.add_neighbor(server_B, 4)
    server_A.add_neighbor(server_C, 2)
   
    server_B.add_neighbor(server_A, 4)
    server_B.add_neighbor(server_C, 5)
    server_B.add_neighbor(server_D, 10)
   
    server_C.add_neighbor(server_A, 2)
    server_C.add_neighbor(server_B, 5)
    server_C.add_neighbor(server_D, 3)
    server_C.add_neighbor(server_E, 2)
   
    server_D.add_neighbor(server_C, 3)
    server_D.add_neighbor(server_B, 10)
    server_D.add_neighbor(server_E, 6)
   
    server_E.add_neighbor(server_D, 6)
    server_E.add_neighbor(server_C,2)
    
    servers = [server_A, server_B, server_C, server_D, server_E]
  
   

    #chemin_plus_court,distance = dijkstra_shortest_path(servers, server_A, server_E)
    #print("Chemin le plus court de A à E:", [server.get_ip() for server in chemin_plus_court])
    #result = BFS(servers, server_A)
    #print("Résultat du BFS:", result)
    
   
  