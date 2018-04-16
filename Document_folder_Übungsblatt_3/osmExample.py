import matplotlib
matplotlib.use('Qt5Agg')
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

# configure osmnx to cache the queries and log what it does
ox.config(use_cache=True, log_console=True)

# use data from file
load_from_file = True

# get the positions of some locations
wachsbleiche = ox.utils.geocode("Wachsbleiche 27, Osnabrück, Deutschland")
harder_example = ox.utils.geocode("Stöppelweg 1, Lengerich, Deutschland")

if load_from_file:
    # load a graph from file
    try:
        G = ox.load_graphml('osnabrueck.graphml', folder='data')
    except FileNotFoundError as e:
        print(e)
        print("fetching data from the web instead")
        G = ox.graph_from_point(wachsbleiche, distance=30000, network_type='drive', simplify=True)
else:
    # fetch it from the osm servers and simplify it
    G = ox.graph_from_point(wachsbleiche, distance=30000, network_type='drive', simplify=True)

# get the closest nodes in the graph for all positions
wachsbleiche_node = ox.get_nearest_node(G, wachsbleiche)
harder_example_node = ox.get_nearest_node(G, harder_example)

# get a route (dijkstra; not the best!!!)
route = nx.shortest_path(G, wachsbleiche_node, harder_example_node)

if route:
    fig, ax = ox.plot_graph_route(G, route, show=False, close=False, axis_off=False, node_color='#66ccff')
else:
    # plot just the graph
    fig, ax = ox.plot_graph(G, show=False, close=False, axis_off=False, annotate=False)

# plot start and end positions of the route (reverse, because the coordinates are returned in the wrong order for matplotlib!)
ax.scatter(*reversed(wachsbleiche), c='r', s=15, zorder=3)
ax.scatter(*reversed(harder_example), c='g', s=15, zorder=3)

# print edge information
for u,v,d in list(G.edges(data=True))[:100]:
    print(u,v,d)

plt.show()


