import tkinter as tk
from tkinter import filedialog
import numpy as np
from stl import mesh
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pymesh

canvas = None
filepath = None
your_mesh = None
axes = None
fig = None
toolbar = None


def rotate(vertices, axis, angle):
    rotation_matrix = np.eye(3)
    cos_angle = np.cos(np.radians(angle))
    sin_angle = np.sin(np.radians(angle))

    if axis == 'x':
        rotation_matrix[1, 1] = cos_angle
        rotation_matrix[1, 2] = -sin_angle
        rotation_matrix[2, 1] = sin_angle
        rotation_matrix[2, 2] = cos_angle
    elif axis == 'y':
        rotation_matrix[0, 0] = cos_angle
        rotation_matrix[0, 2] = sin_angle
        rotation_matrix[2, 0] = -sin_angle
        rotation_matrix[2, 2] = cos_angle
    elif axis == 'z':
        rotation_matrix[0, 0] = cos_angle
        rotation_matrix[0, 1] = -sin_angle
        rotation_matrix[1, 0] = sin_angle
        rotation_matrix[1, 1] = cos_angle

    return np.dot(vertices, rotation_matrix)


def update_plot(rotated_vectors):
    global your_mesh
    axes.clear()
    poly3d = Poly3DCollection(
        rotated_vectors, facecolors='gray', edgecolor='black')
    axes.add_collection3d(poly3d)
    scale = your_mesh.vertices.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    fig.canvas.draw()


def on_key(event):
    global your_mesh

    if event.key == 'up':
        your_mesh.vertices = rotate(your_mesh.vertices, 'x', 5)
    elif event.key == 'down':
        your_mesh.vertices = rotate(your_mesh.vertices, 'x', -5)
    elif event.key == 'left':
        your_mesh.vertices = rotate(your_mesh.vertices, 'y', 5)
    elif event.key == 'right':
        your_mesh.vertices = rotate(your_mesh.vertices, 'y', -5)
    update_plot(your_mesh.vertices)


def on_scroll(event):
    # get the current zoom factor
    fov = axes.dist
    if event.button == 'up':
        # zoom in
        fov = (1 - 0.1) * fov
    elif event.button == 'down':
        # zoom out
        fov = (1 + 0.1) * fov
    if fov > 0.01:
        axes.dist = fov
        plt.draw()


def generate_stl():
    global your_mesh
    global canvas
    global filepath
    global axes
    global fig
    global toolbar

    filepath = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
    if not filepath:
        return
    your_mesh = mesh.Mesh.from_file(filepath)

    # Flatten the points array to get all vertices, and then find unique vertices
    all_points = your_mesh.points.reshape(-1, 3)
    unique_points, unique_indices = np.unique(
        all_points, axis=0, return_inverse=True)
    num_points = len(unique_points)

    # Reindex the points array with the indices of the unique vertices
    reindexed_points = unique_indices.reshape(-1, 3)

    # Create a set to store the unique edges
    edges_set = set()

    # For each face, add all the edges to the set
    for face in reindexed_points:
        for i in range(3):
            # Create a tuple for each edge, sorted to ensure the same edge
            # isn't counted twice just because the vertices are in a different order
            edge = tuple(sorted([face[i], face[(i+1) % 3]]))
            edges_set.add(edge)

    num_edges = len(edges_set)  # Count of unique edges
    num_faces = your_mesh.vectors.shape[0]

    # Update the labels
    update_labels(num_points, num_edges, num_faces)

    rotated_vectors = rotate(your_mesh.vectors, 'x', 0)
    # Rotate 30 degrees around the y-axis
    rotated_vectors = rotate(rotated_vectors, 'y', 0)
    # Rotate 30 degrees around the z-axis
    rotated_vectors = rotate(rotated_vectors, 'z', 270)
    fig = plt.figure(figsize=(5, 5))
    axes = fig.add_subplot(111, projection='3d')
    poly3d = Poly3DCollection(
        rotated_vectors, facecolors='gray', edgecolor='black')
    axes.add_collection3d(poly3d)
    fig.canvas.mpl_connect('key_press_event', on_key)
    fig.canvas.mpl_connect('scroll_event', on_scroll)

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    if canvas is not None:
        canvas.get_tk_widget().destroy()
        toolbar.destroy()

    # Prepare the data for Poly3DCollection

    canvas = FigureCanvasTkAgg(fig, master=root)

    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)


def simulate_airflow():
    # code to simulate airflow against STL file goes here
    pass


def update_labels(points, edges, faces):
    points_label['text'] = f"Number of unique points: {points}"
    edges_label['text'] = f"Number of edges: {edges}"
    faces_label['text'] = f"Number of faces: {faces}"


root = tk.Tk()
root.title("CCTSN")
window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}")

generate_button = tk.Button(root, text="Load STL File", command=generate_stl)
generate_button.pack()

points_label = tk.Label(root, text="")
points_label.pack()

edges_label = tk.Label(root, text="")
edges_label.pack()

faces_label = tk.Label(root, text="")
faces_label.pack()

simulate_button = tk.Button(
    root, text="Simulate Airflow", command=simulate_airflow)
simulate_button.pack()

root.mainloop()
