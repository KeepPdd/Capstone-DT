import random
from typing import List, Tuple, Set
import numpy as np

Point = Tuple[float, float]
Triangle = Tuple[Point, Point, Point]

def normalize_triangle(t: Triangle) -> Triangle:
    """Returns a normalized (sorted) version of the triangle for consistent hashing."""
    return tuple(sorted(t))

def dist2(p1: Point, p2: Point) -> float:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def orient(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def in_circle(a: Point, b: Point, c: Point, d: Point) -> bool:
    orientation = orient(a, b, c)
    mat = [
        [a[0], a[1], a[0]**2 + a[1]**2, 1],
        [b[0], b[1], b[0]**2 + b[1]**2, 1],
        [c[0], c[1], c[0]**2 + c[1]**2, 1],
        [d[0], d[1], d[0]**2 + d[1]**2, 1]
    ]
    det = np.linalg.det(mat)
    return det > 0 if orientation > 0 else det < 0

def point_in_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    area = abs(orient(a, b, c))
    if area == 0:
        return False
    w1 = orient(p, b, c)
    w2 = orient(p, c, a)
    w3 = orient(p, a, b)
    return (w1 >= 0 and w2 >= 0 and w3 >= 0) or (w1 <= 0 and w2 <= 0 and w3 <= 0)

def incremental_delaunay(points: List[Point]) -> List[Triangle]:
    points = points.copy()
    random.shuffle(points)

    # Super triangle (huge triangle enclosing all points)
    inf = 4e2
    p1 = (-inf, -inf)
    p2 = (0, inf)
    p3 = (inf, -inf)
    super_points = {p1, p2, p3}
    triangles: Set[Triangle] = {normalize_triangle((p1, p2, p3))}

    def legalize_triangle(t: Triangle):
        a, b, c = t
        edges = [(a, b), (b, c), (c, a)]  # All edges of the triangle
        for u, v in edges:
            # Find the triangle sharing edge uv
            for other in triangles:
                if other == t:
                    continue
                shared = {u, v}
                if shared <= set(other):  # Check if edge is shared
                    # Get the opposite point in the other triangle
                    opp = next(p for p in other if p not in shared)
                    if in_circle(u, v, next(p for p in t if p not in shared), opp):
                        # Flip edge
                        new_t1 = normalize_triangle((next(p for p in t if p not in shared), opp, u))
                        new_t2 = normalize_triangle((next(p for p in t if p not in shared), opp, v))
                        
                        triangles.remove(t)
                        triangles.remove(other)
                        triangles.add(new_t1)
                        triangles.add(new_t2)
                        
                        # Recursively legalize new triangles
                        legalize_triangle(new_t1)
                        legalize_triangle(new_t2)
                    break  # Each edge can only be shared by one other triangle

    for p in points:
        # Find all triangles whose circumcircle contains p
        bad_triangles = set()
        for tri in triangles:
            a, b, c = tri
            if in_circle(a, b, c, p):
                bad_triangles.add(tri)
        
        # Find the boundary of the polygonal hole
        polygon_edges = []
        for tri in bad_triangles:
            for edge in [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]:
                edge = tuple(sorted(edge))
                shared = sum(1 for t in bad_triangles if edge[0] in t and edge[1] in t)
                if shared == 1:  # Boundary edge
                    polygon_edges.append(edge)
        
        # Remove bad triangles
        triangles -= bad_triangles
        
        # Create new triangles with p and each boundary edge
        for edge in polygon_edges:
            new_tri = normalize_triangle((edge[0], edge[1], p))
            triangles.add(new_tri)
    
    # Remove super triangle
    triangles = {tri for tri in triangles if not super_points & set(tri)}

    return list(triangles)

def incremental_delaunay_dummy(points: List[Point]) -> List[Triangle]:
    points = points.copy()
    random.shuffle(points)

    # Super triangle (huge triangle enclosing all points)
    inf = 4e2
    p1 = (-inf, -inf)
    p2 = (0, inf)
    p3 = (inf, -inf)
    super_points = {p1, p2, p3}
    triangles: Set[Triangle] = {normalize_triangle((p1, p2, p3))}

    def legalize_triangle(t: Triangle):
        a, b, c = t
        edges = [(a, b), (b, c), (c, a)]  # All edges of the triangle
        for u, v in edges:
            # Find the triangle sharing edge uv
            for other in triangles:
                if other == t:
                    continue
                shared = {u, v}
                if shared <= set(other):  # Check if edge is shared
                    # Get the opposite point in the other triangle
                    opp = next(p for p in other if p not in shared)
                    if in_circle(u, v, next(p for p in t if p not in shared), opp):
                        # Flip edge
                        new_t1 = normalize_triangle((next(p for p in t if p not in shared), opp, u))
                        new_t2 = normalize_triangle((next(p for p in t if p not in shared), opp, v))
                        
                        triangles.remove(t)
                        triangles.remove(other)
                        triangles.add(new_t1)
                        triangles.add(new_t2)
                        
                        # Recursively legalize new triangles
                        legalize_triangle(new_t1)
                        legalize_triangle(new_t2)
                    break  # Each edge can only be shared by one other triangle

    for p in points:
        # Find all triangles whose circumcircle contains p
        bad_triangles = set()
        for tri in triangles:
            a, b, c = tri
            if in_circle(a, b, c, p):
                bad_triangles.add(tri)
        
        # Find the boundary of the polygonal hole
        polygon_edges = []
        for tri in bad_triangles:
            for edge in [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]:
                edge = tuple(sorted(edge))
                shared = sum(1 for t in bad_triangles if edge[0] in t and edge[1] in t)
                if shared == 1:  # Boundary edge
                    polygon_edges.append(edge)
        
        # Remove bad triangles
        triangles -= bad_triangles
        
        # Create new triangles with p and each boundary edge
        for edge in polygon_edges:
            new_tri = normalize_triangle((edge[0], edge[1], p))
            triangles.add(new_tri)
    
    # Remove super triangle
    triangles = {tri for tri in triangles if not super_points & set(tri)}