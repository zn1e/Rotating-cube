import pygame
import numpy as np
import math

# Initialize pygame
pygame.init() 

# Setup configurations 
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define cube's vertices
VERTICES = np.array([[-1, -1, -1],
                     [1, -1, -1],
                     [1, 1, -1],
                     [-1, 1, -1],
                     [-1, -1, 1],
                     [1, -1, 1],
                     [1, 1, 1,],
                     [-1, 1, 1]])

# Define edges connecting each vertices
EDGES = [(0, 1), (1, 2), (2, 3), (3, 0),
         (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]


def rotation_matrix(axis, theta):
    """Returns the rotation matrix for the given axis and theta.
    Source: Basic 3D Rotations @ Rotation matrix wikipedia
    """
    if axis == 'x':
        return np.array([[1, 0, 0],
                        [0, math.cos(theta), -math.sin(theta)],
                        [0, math.sin(theta), math.cos(theta)]])
    elif axis == 'y':
        return np.array([[math.cos(theta), 0, math.sin(theta)],
                        [0, 1, 0],
                        [-math.sin(theta), 0, math.cos(theta)]])
    elif axis == 'z':
        return np.array([[math.cos(theta), -math.sin(theta), 0],
                        [math.sin(theta), math.cos(theta), 0],
                        [0, 0, 1]])
    

def project(points):
    """Project the points from 3D to 2D for pygame processing."""
    scale = 400
    camera_distance = 4
    
    projection_matrix = np.array([[1, 0, 0],
                                 [0, 1, 0]])
    points = points / (camera_distance - points[:, 2].reshape(-1, 1))
    points = np.dot(points, projection_matrix.T)
    points = scale * points + np.array([WIDTH // 2, HEIGHT // 2])
    return points


def main():
    """Main function that calls the rotation of the cube in pygame
    environment.
    """
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle_x += 0.005
        angle_y += 0.005
        angle_y += 0.005

        rotation_x = rotation_matrix('x', angle_x)
        rotation_y = rotation_matrix('y', angle_y)
        rotation_z = rotation_matrix('z', angle_z)

        rotated_vertices = np.dot(VERTICES, rotation_x)
        rotated_vertices = np.dot(rotated_vertices, rotation_y)
        rotated_vertices = np.dot(rotated_vertices, rotation_z)

        projected_vertices = project(rotated_vertices)

        SCREEN.fill(BLACK)

        for edge in EDGES:
            points = [projected_vertices[edge[0]], projected_vertices[edge[1]]]
            pygame.draw.line(SCREEN, WHITE, points[0], points[1], 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

