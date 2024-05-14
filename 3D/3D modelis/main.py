import math
import random

def coral_function(u, v):
    x = (2 + math.cos(7 * u)) * math.cos(u) * math.cos(v)
    y = (2 + math.cos(7 * u)) * math.sin(u) * math.cos(v)
    z = math.sin(7 * u) * math.sin(v)
    return x, y, z

def flower_petals(u, v):
    petal_scale = 0.2
    angle_offset = math.pi / 2 
    x = petal_scale * (math.cos(u) * math.cos(v) * math.sin(u) * math.cos(v + angle_offset))
    y = petal_scale * (math.cos(u) * math.sin(v) * math.sin(u) * math.cos(v + angle_offset))
    z = petal_scale * math.sin(u) * math.sin(v + angle_offset)
    return x, y, z

def calculate_color(vertex):
    z_min = -2.0  
    z_max = 2.0  
    z = vertex[2]  
    blue = max(0, min(1, (z - z_min) / (z_max - z_min)))  
    red = 1 - blue  
    green = 0.0  
    color = (red, green, blue)  
    return color

def save_to_obj(vertices, faces, colors, filename):
    with open(filename, 'w') as f:
        for i, vertex in enumerate(vertices):
            color = colors[i]
            f.write("v {} {} {} {} {} {}\n".format(vertex[0], vertex[1], vertex[2], color[0], color[1], color[2]))
        for face in faces:
            f.write("f {} {} {}\n".format(face[0], face[1], face[2]))

def main():
    resolution = 100

    vertices = []
    colors = []
    for i in range(resolution):
        for j in range(resolution):
            u = 2 * math.pi * i / resolution
            v = 2 * math.pi * j / resolution
            vertex = coral_function(u, v)
            vertices.append(vertex)
            color = calculate_color(vertex)
            colors.append(color)

    faces = []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            idx1 = i * resolution + j + 1
            idx2 = i * resolution + (j + 1) + 1
            idx3 = (i + 1) * resolution + (j + 1) + 1
            idx4 = (i + 1) * resolution + j + 1
            faces.append((idx1, idx2, idx3))
            faces.append((idx1, idx3, idx4))

    flower_points = []
    flower_resolution = 100
    for i in range(flower_resolution):
        u = 2 * math.pi * random.random()
        v = 2 * math.pi * random.random()
        flower_points.append(flower_petals(u, v))

    for i in range(len(flower_points)):
        vertices.append(flower_points[i])
        colors.append((1.0, 0.6, 0.8))  
        if i > 0:
            faces.append((len(vertices) - 1, len(vertices) - 2, len(vertices) - 2 - flower_resolution))
            faces.append((len(vertices) - 1, len(vertices) - 2 - flower_resolution, len(vertices) - 1 - flower_resolution))

    save_to_obj(vertices, faces, colors, 'dekoracija.obj')

if _name_ == "_main_":
    main()