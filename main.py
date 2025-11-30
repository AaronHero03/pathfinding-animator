import osmnx as ox
import random
import heapq
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os
import imageio.v2 as imageio
import shutil

# Load graph map with osmnx
center_point = (21.122, -101.680)  # latitude, longitude
G = ox.graph_from_point(center_point, dist=7000, network_type="drive") # Square 7 km around the center point
G = ox.project_graph(G) 

# Output paramethers
fps = 40
size = 10
animation = True
frames_folder = "Try"

# Global variables
stage = "finding"
os.makedirs(frames_folder, exist_ok=True)
frame_count = 0

# Clean speed atribute on the edges
for u, v, key, data in G.edges(keys=True, data=True):
    maxspeed = 60
    if "maxspeed" in data:
        val = data['maxspeed']
        if isinstance(val, list):
            val = min([int(''.join(filter(str.isdigit, s))) for s in val])
        elif isinstance(val, str):
            val = int(''.join(filter(str.isdigit, val)))
        maxspeed = val
    data["maxspeed"] = maxspeed
    data["weight"] = data["length"] / maxspeed

# Style utils
def style_unvisited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 0.2
    G.edges[edge]["linewidth"] = 0.5

def style_visited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_active_edge(edge):
    G.edges[edge]["color"] = '#e8a900'
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_path_edge(edge):
    G.edges[edge]["color"] = "white"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_start_end(node):
    G.nodes[node]["highlight"] = True
    G.nodes[node]["size"] = 25 
    G.nodes[node]["color"] = "#FFFFFF"

# Get position of each node
pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Build edges 
edges_lines = []
edges_keys = []
for u, v, key, data in G.edges(keys=True, data=True):
    edges_keys.append((u,v,key))
    if 'geometry' in data:
        coords = list(data['geometry'].coords)
    else:
        coords = [pos[u], pos[v]]
    edges_lines.append(coords)

# Create LineCollection to setup the map
lc = LineCollection(edges_lines,
                    colors=[G.edges[e].get('color', '#d36206') for e in edges_keys],
                    linewidths=[G.edges[e].get('linewidth',0.5) for e in edges_keys],
                    alpha=[G.edges[e].get('alpha',0.2) for e in edges_keys])

# Plot paramethers
fig, ax = plt.subplots(figsize=(size,size))
fig.patch.set_facecolor("#18080e")
ax.set_facecolor("#18080e")    

# Add Line collection to the plot
ax.add_collection(lc)
ax.set_xlim(min(x for x, y in pos.values()), max(x for x, y in pos.values()))
ax.set_ylim(min(y for x, y in pos.values()), max(y for x, y in pos.values()))
ax.axis('off')

# Function to save a frame of the execution
def save_frame(step):
    global frame_count, stage

    if stage == "finding":
        if step % 32 != 0:
            return    
    elif stage == "reconstructing":
        if step % 3 != 0:
            return 
    elif stage == "found":
        pass

    lc.set_color([G.edges[e].get('color', '#d36206') for e in edges_keys])
    lc.set_linewidth([G.edges[e].get('linewidth',0.5) for e in edges_keys])
    lc.set_alpha([G.edges[e].get('alpha',0.2) for e in edges_keys])

    highlighted = [n for n, data in G.nodes(data=True) if data.get("highlight")]
    ax.scatter([pos[n][0] for n in highlighted],
           [pos[n][1] for n in highlighted],
           s=[G.nodes[n]["size"] for n in highlighted],
           c=[G.nodes[n]["color"] for n in highlighted],
           zorder=3)

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.savefig(os.path.join(frames_folder, f"frame_{frame_count:05d}.png"),
                dpi=160, facecolor=fig.get_facecolor(), transparent=False)
    frame_count += 1

# Dijkstra's Algorithm
def dijkstra(orig, dest, isAnimate=False):
    global stage
    stage = "finding"

    # Setup attributes of each node
    for node in G.nodes:
        G.nodes[node]["visited"] = False
        G.nodes[node]["distance"] = float("inf")
        G.nodes[node]["previous"] = None
        G.nodes[node]["size"] = 0

    # Setup algorithm
    for edge in G.edges:
        style_unvisited_edge(edge)

    G.nodes[orig]["distance"] = 0
    style_start_end(orig)
    style_start_end(dest)
    pq = [(0, orig)]
    step = 0


    while pq:
        _, node = heapq.heappop(pq)

        if node == dest:
            stage = "found"
            if isAnimate:
                for _ in range(22):
                    save_frame(step)
            else:
                save_frame(step)
            return step
        

        if G.nodes[node]["visited"]: 
            continue
        G.nodes[node]["visited"] = True
        
        # Relax vertex 
        for edge in G.out_edges(node, keys=True):
            style_visited_edge(edge)
            neighbor = edge[1]
            weight = G.edges[edge]["weight"]
            if G.nodes[neighbor]["distance"] > G.nodes[node]["distance"] + weight:
                G.nodes[neighbor]["distance"] = G.nodes[node]["distance"] + weight
                G.nodes[neighbor]["previous"] = node
                heapq.heappush(pq, (G.nodes[neighbor]["distance"], neighbor))

                # Update style of the visited edges
                for edge2 in G.out_edges(neighbor, keys=True):
                    style_active_edge(edge2)
        
        # Plot frame
        if isAnimate:
            save_frame(step)
        step += 1
    return step

# Reconstruct shortest route
def reconstruct_path(orig, dest, isAnimate=False, algorithm=None):
    global stage
    stage = "reconstructing"        
    # Turn off all the edges
    for edge in G.edges:
        style_unvisited_edge(edge)
    dist = 0
    speeds = []
    curr = dest
    step = 0

    # Go throw the previous until found the origin
    while curr != orig:
        prev = G.nodes[curr]["previous"]
        if prev is None:
            print("Unnaccessible goal")
            return
        
        for key in G[prev][curr]:
            style_path_edge((prev,curr,key))
            if algorithm:
                G.edges[(prev,curr,key)][f"{algorithm}_uses"] = G.edges[(prev,curr,key)].get(f"{algorithm}_uses",0)+1
        dist += G.edges[(prev,curr,0)]["length"]
        speeds.append(G.edges[(prev,curr,0)]["maxspeed"])
        curr = prev
        if isAnimate:
            save_frame(step)
        step += 1
    
    # Distance in kilometers
    dist /= 1000

    print(f"Distance: {dist} km")
    print(f"Avg. speed: {sum(speeds)/len(speeds)}")
    print(f"Total time: {dist/(sum(speeds)/len(speeds)) * 60} min")

    if not isAnimate:
        stage = "found"
        save_frame(step)

# Generate an animation of the algorithm
def generate_video(frames_folder, output_video):
    frames = sorted([
    os.path.join(frames_folder, f)
    for f in os.listdir(frames_folder)
    if f.endswith(".png")
    ])

    # Crear video
    with imageio.get_writer(output_video, fps=fps, codec='libx264') as writer:
        for frame in frames:
            writer.append_data(imageio.imread(frame))

    print("Video generado exitosamente:", output_video)

    # Clean frames
    shutil.rmtree(frames_folder)
    print("Carpeta de frames eliminada.")

start = random.choice(list(G.nodes))
end = random.choice(list(G.nodes))

total_steps = dijkstra(start, end, isAnimate=animation)
reconstruct_path(start, end, isAnimate=animation)

if animation:
    generate_video(frames_folder,"output.mp4")