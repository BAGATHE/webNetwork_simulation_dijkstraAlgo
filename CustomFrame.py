import tkinter as tk
import Server 
from Server import Server
from Server import dijkstra_shortest_path
from Server import BFS
from tkinter import messagebox



class CustomFrame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dual Canvas App")
        self.geometry("1200x800")

        self.canvas1 = None
        self.canvas2 = None
        self.servers = []
        self.create_widgets()
    """ CREATION DEUX 2 PANEL DANS LE FRAME"""
    def create_widgets(self):
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    # Premier canvas avec un arrière-plan
        self.canvas1 = tk.Canvas(canvas_frame, bg="white", width=1000)
        self.canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        # Charger l'image de fond
        self.background_image = tk.PhotoImage(file="image/back11.png")
        # Créer une image sur le canevas avec l'image de fond
        self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    # Positionner l'image de fond au-dessous de tous les autres éléments
        self.canvas1.lower(self.background_image)
    
        self.canvas1.bind("<Button-3>", self.show_canvas_menu)
        self.canvas1.bind("<ButtonRelease-2>", self.on_drag_end)
    
    # Deuxième canvas
        self.canvas2 = tk.Canvas(canvas_frame, bg="lightgray", width=200)
        self.canvas2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


      
    """----------------------> MENU CLIQUE DROITE<---------------------------------------- """
    def show_canvas_menu(self, event):
        # Créer le menu
        canvas_menu = tk.Menu(self, tearoff=0)
        canvas_menu.add_command(label="Add Server in location", command=self.show_form_server)
        # Afficher le menu au pointeur de la souris
        canvas_menu.post(event.x_root, event.y_root)
    
    def show_form_server(self):
        for widget in self.canvas2.winfo_children():
            widget.destroy()
        x, y = self.canvas1.winfo_pointerxy()
        default_position_x = x
        default_position_y = y

        label_ip = tk.Label(self.canvas2, text="IP:")
        label_ip.pack()

        entry_ip = tk.Entry(self.canvas2)
        entry_ip.pack()

        label_pos_x = tk.Label(self.canvas2, text="Position X:")
        label_pos_x.pack()

        entry_pos_x = tk.Entry(self.canvas2)
        entry_pos_x.insert(0, str(default_position_x))
        entry_pos_x.pack()

        label_pos_y = tk.Label(self.canvas2, text="Position Y:")
        label_pos_y.pack()

        entry_pos_y = tk.Entry(self.canvas2)
        entry_pos_y.insert(0, str(default_position_y))
        entry_pos_y.pack()
        btn_validate = tk.Button(self.canvas2, text="Valider", command=lambda: self.add_server(entry_ip.get(), entry_pos_x.get(), entry_pos_y.get()))
        btn_validate.pack()
    
    #AJOUTER SERVER SUR LE CANEVAS
    def add_server(self,ip_address,pos_x,pos_y):
     
        canvas_x = self.canvas1.winfo_rootx()
        canvas_y = self.canvas1.winfo_rooty()
        x = int(pos_x)
        y = int(pos_y)
        x -= canvas_x
        y -= canvas_y
        server_image = tk.PhotoImage(file="image/data-storage1.png")
        server_image_id = self.canvas1.create_image(x, y, anchor=tk.CENTER, image=server_image)
        ip_text = self.canvas1.create_text(x, y + 30, text=ip_address, fill="red", font=("Arial", 10), anchor=tk.CENTER)
    
        server = Server(ip_address)
        server.set_ipId(ip_text)
        server.set_image(server_image)
        server.set_points([x,y])
        server.set_idImage(server_image_id)
        server_data = server
        self.servers.append(server_data)

        self.canvas1.tag_bind(server_data.get_idImage(), "<Button-2>", lambda event, server_data=server_data: self.show_option_server(event,server_data))
        self.canvas1.tag_bind(server_data.get_idImage(), "<ButtonPress-1>", lambda event, server_data=server_data: self.on_drag_start(server_data))
        self.canvas1.tag_bind(server_data.get_idImage(), "<B1-Motion>", lambda event, server_data=server_data: self.on_drag_motion(event,server_data))
    
    
    #FONCTION QUI RECUPERER COORDONNER X ET Y AU CLIQUE DU SERVER
    def on_drag_start(self, server_data):
    # Enregistrer les données du serveur en cours de déplacement
        self.dragging_server = server_data
        self.start_x = server_data.get_points()[0]
        self.start_y = server_data.get_points()[1]
     
         
    def on_drag_motion(self, event,server_data):
        if self.dragging_server:
            x_delta =  event.x - self.start_x
            y_delta =  event.y - self.start_y
            server_image_id = self.dragging_server.get_idImage()
            self.canvas1.coords(server_image_id, self.start_x + x_delta, self.start_y + y_delta)
            ip_address_Id = self.dragging_server.get_ipId()
            self.canvas1.coords(ip_address_Id,self.start_x + x_delta ,self.start_y + y_delta + 30)
          
            newx =self.start_x + x_delta
            newy = self.start_y + y_delta
            server_data.set_points([newx,newy])

            linked_servers = server_data.get_neighbors()
            for linked_server in linked_servers:
                indice = 0
                for id_line in linked_server[0].get_line():
                    if id_line in server_data.get_line():
                        x1, y1 = server_data.get_points()
                        x2, y2 = linked_server[0].get_points()
                        self.canvas1.coords(id_line, x1, y1, x2, y2)
                    if  linked_server[0].get_refping()[indice] in server_data.get_refping():
                        x1, y1 = server_data.get_points()
                        x2, y2 = linked_server[0].get_points()
                        self.canvas1.coords(linked_server[0].get_refping()[indice], (x1 + x2) / 2, ((y1 + y2) / 2) - 5)
                    indice+=1
                

 

    def on_drag_end(self, event):
    # Supprimer les données du serveur en cours de déplacement
        self.dragging_server = None
    
    
    
    
    
    """------------------------>MENU CLIQUE ROULETTE<--------------------------------"""
    def show_option_server(self, event,server_data):
        menu = tk.Menu(self, tearoff=0)
        menu.add_separator()
        menu.add_command(label="Add site", command=lambda : self.show_form_AddSite(server_data.get_ip()))
        menu.add_separator()
        menu.add_command(label="Add Link", command= self.show_form_link)
        menu.add_separator()
        menu.add_command(label="Search site", command=lambda :self.show_form_search(server_data.get_ip()))
        menu.add_separator()
        menu.add_command(label="show hosted Site", command=lambda :self.show_hosteds_site(server_data.get_ip()))
        menu.post(event.x_root, event.y_root)
    
    #FORMULAIRE AJOUTER SITE
    def show_form_AddSite(self,ip):
        for widget in self.canvas2.winfo_children():
            widget.destroy()
    # Créer les labels et les champs d'entrée pour les adresses IP et le poids
        label_ip = tk.Label(self.canvas2, text="IP Server :")
        label_ip.pack()

        entry_ip = tk.Entry(self.canvas2)
        entry_ip.insert(0, str(ip))
        entry_ip.pack()

        label_list_site = tk.Label(self.canvas2, text="List site:")
        label_list_site.pack()

        entry_list_site = tk.Entry(self.canvas2)
        entry_list_site.pack()

         # Bouton de validation avec la fonction de gestion de validation
        btn_validate = tk.Button(self.canvas2, text="Valider", command=lambda: self.add_Site(entry_ip.get(), entry_list_site.get()))
        btn_validate.pack()
    
    #FONCTION AJOUTER SITE DANS SERVERS
    def add_Site(self, ipServer, listSiteString):
        server = Server.get_Server_by_ip(ipServer,self.servers)
        server_list = listSiteString.split(",")
       
        message = "Les sites ajoutés sont :\n"
        for site in server_list:
            server.add_hostedSiteList(site)
            message += f"- {site}\n"

        # Afficher une boîte de message avec la liste des sites ajoutés
        messagebox.showinfo("Sites ajoutés", message)
        self.load_list_site_byServer()
    
    def load_list_site_byServer(self):
        xip, yip = 50, 700
        for server in self.servers:
            self.canvas1.create_text(xip, yip, text=server.get_ip(), fill="red", font=("Arial", 10), anchor=tk.CENTER)
            distance = 10
            for site in server.get_hostedSiteList():
                yip += distance  # Adjusting y-coordinate for each site
                self.canvas1.create_text(xip, yip, text=site, fill="blue", font=("Arial", 10), anchor=tk.CENTER)
                distance +=5   # Increasing distance for next site
            xip += 100
            yip = 700

    #FORMULAIRE AJOUTER LIEN ENTRE DEUX SERVER
    def show_form_link(self):
        for widget in self.canvas2.winfo_children():
            widget.destroy()

        label_ip1 = tk.Label(self.canvas2, text="IP Server 1:")
        label_ip1.pack()

        entry_ip1 = tk.Entry(self.canvas2)
        entry_ip1.pack()

        label_ip2 = tk.Label(self.canvas2, text="IP Server 2:")
        label_ip2.pack()

        entry_ip2 = tk.Entry(self.canvas2)
        entry_ip2.pack()

        label_weight = tk.Label(self.canvas2, text="Ping:")
        label_weight.pack()

        entry_weight = tk.Entry(self.canvas2)
        entry_weight.pack()

        btn_validate = tk.Button(self.canvas2, text="Valider", command=lambda: self.add_link(entry_ip1.get(), entry_ip2.get(), entry_weight.get()))
        btn_validate.pack()
    
    def add_link(self, ip1, ip2, ping):
        
        ping = int(ping)
        server1 = Server.get_Server_by_ip(ip1,self.servers)
        server2 = Server.get_Server_by_ip(ip2,self.servers)
        if server1 is not None and server2 is not None:
        # Dessiner une ligne entre les serveurs sur le canevas
            x1, y1 = server1.get_points()
            x2, y2 = server2.get_points()
            line_id = self.canvas1.create_line(x1, y1, x2, y2, fill="blue", width=2)
            ping_id = self.canvas1.create_text((x1 + x2) / 2, ((y1 + y2) / 2)-5, text=f"{ping} ms", fill="red", font=("Arial", 15))
            server1.add_refping(ping_id)
            server2.add_refping(ping_id)
            server1.get_line().append(line_id)
            server2.get_line().append(line_id)
            server1.add_neighbor(server2, ping)
            server2.add_neighbor(server1, ping)
        else:
            print("Erreur: Impossible de trouver les serveurs correspondant aux adresses IP spécifiées.")

    #FORMULAIRE RECHERCHER URL 
    def show_form_search(self,ipServer):
        for widget in self.canvas2.winfo_children():
            widget.destroy()

        label_ip = tk.Label(self.canvas2, text="IP Server :")
        label_ip.pack()

        entry_ip = tk.Entry(self.canvas2)
        entry_ip.insert(0, str(ipServer))
        entry_ip.pack()

        label_url = tk.Label(self.canvas2, text="url search:")
        label_url.pack()

        entry_url = tk.Entry(self.canvas2)
        entry_url.pack()
        
        btn_validate = tk.Button(self.canvas2, text="Valider", command=lambda: self.search_path_site(entry_ip.get(), entry_url.get(),self.servers))
    
        btn_validate.pack()
    
    def change_link_color(self, server1, server2, new_color):
        if server1 is not None and server2 is not None:
            for line_id in server1.get_line():
                if line_id in server2.get_line():
                    self.canvas1.itemconfig(line_id, fill=new_color)
                    break  # Sortir de la boucle si l'ID de ligne est trouvé et la couleur est modifiée
        else:
            print("Erreur: Impossible de trouver les serveurs correspondant aux adresses IP spécifiées.")
    
    def change_path_color(self, server1, server2, new_color):
        if server1 is not None and server2 is not None:
            for line_id in server1.get_line():
                if line_id in server2.get_line():
                    self.canvas1.itemconfig(line_id, fill=new_color, width=3, dash=(5, 2), stipple='gray50')
                    break  # Sortir de la boucle si l'ID de ligne est trouvé et la couleur est modifiée
        else:
            print("Erreur: Impossible de trouver les serveurs correspondant aux adresses IP spécifiées.")





    #AFFICHAGE LISTE SITE DANS UN SERVERS
    def show_hosteds_site(self,ip):
        server = Server.get_Server_by_ip(ip,self.servers)
        message = "Les sites hebergé sont :\n"
        for site in server.get_hostedSiteList():
            message += f"- {site}\n"
        messagebox.showinfo("Sites hebergé", message)

    def findIndice_min_distance(self,tabDistance):
        mindist = tabDistance[0][1]
        indice=0
        for i in range (1,len(tabDistance)):
            if mindist > tabDistance[i][1]:
                mindist = tabDistance[i][1]
                indice = i
        return indice
    
    # def search_path_site(self, ipServer, url, list_servers):
    #     for server in self.servers:
    #         for line_id in server.get_line():
    #             self.canvas1.itemconfig(line_id, fill="blue", dash=(), stipple='')

        
    #     source = Server.get_Server_by_ip(ipServer,self.servers)
    #     server_list_hosting_site = Server.find_servers_hosting_site(source,url,list_servers)
    #     tabDistance = []
    #     tabPathshortest = []
    #     indice = 0
    #     for destination in server_list_hosting_site:
    #         chemin_plus_court,distance = dijkstra_shortest_path(self.servers,source,destination)
    #         tabPathshortest.append(chemin_plus_court)
    #         tabDistance.append([indice,distance])
    #         if chemin_plus_court:
    #             for i in range(len(chemin_plus_court)-1):
    #                 self.change_link_color(chemin_plus_court[i],chemin_plus_court[i+1],"yellow")
    #         indice+=1
    #     min_distance_indice = self.findIndice_min_distance(tabDistance)
    #     shorted_path = tabPathshortest[min_distance_indice]
    #     for i in range(len(shorted_path)-1):
    #         self.change_path_color(shorted_path[i],shorted_path[i+1],"red")
    

    def search_path_site(self, ipServer, url, list_servers):
        for server in self.servers:
            for line_id in server.get_line():
                self.canvas1.itemconfig(line_id, fill="blue", dash=(), stipple='')

        
        source = Server.get_Server_by_ip(ipServer,self.servers)
        server_list_hosting_site = Server.find_servers_hosting_site(source,url,list_servers)
        
        tabPathshortest = []
        indice = 0
        for destination in server_list_hosting_site:
            chemin_plus_court = BFS(self.servers,source,destination)
            tabPathshortest.append(chemin_plus_court)
            if chemin_plus_court:
                for i in range(len(chemin_plus_court)-1):
                    self.change_link_color(chemin_plus_court[i],chemin_plus_court[i+1],"yellow")
            
        
    
   



            
        

    
    
    
       
      
    
 

    

 

    
    
    

    
    
    