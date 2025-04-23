import math
import random
import numpy as np
from typing import List, Tuple

Point = Tuple[float, float]

# Helper functions for geometry

def angle(p: Point, q: Point, r: Point) -> float:
    # 返回 ∠qpr 的夹角（弧度）
    v1 = (q[0] - p[0], q[1] - p[1])
    v2 = (r[0] - p[0], r[1] - p[1])
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    len1 = math.hypot(*v1)
    len2 = math.hypot(*v2)
    if len1 == 0 or len2 == 0:
        return -math.inf
    cos_theta = dot / (len1 * len2)
    return math.acos(max(-1, min(1, cos_theta)))

def dist2(p1: Point, p2: Point) -> float:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def orient(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def in_circle(a: Point, b: Point, c: Point, d: Point) -> bool:
    # Check if point d lies inside the circumcircle of triangle abc
    # Uses determinant method
    orientation=orient(a,b,c)
    mat = [
        [a[0] , a[1],a[0]**2+a[1]**2 ,1],
        [b[0] , b[1],b[0]**2+b[1]**2 ,1],
        [c[0] , c[1],c[0]**2+c[1]**2 ,1],
        [d[0] , d[1],d[0]**2+d[1]**2 ,1]
    ]
    det = np.linalg.det(mat)
    if orientation > 0:
        return det > 0
    else:
        return det < 0

def first_delaunay_edge(p: Point, S: List[Point]) -> Point:
    # Find the closest point to p in S
    candidates = [q for q in S if q != p]
    if not candidates:
        raise ValueError("No valid candidate points in the set S.")
    return min(candidates, key=lambda q: dist2(p, q))


def clockwise_next_edge(p: Point, q: Point, S: List[Point]) -> Point:
    # Clockwise next Delaunay edge incident to p following edge pq
    global flag
    flag=True
    r_candidate = None
    for r in S:
        if r == p or r == q:
            continue
        if orient(p, q, r) >= 0:
            continue  # only consider points to the right of pq
        if r_candidate is None or in_circle(p, q, r_candidate, r):
            r_candidate = r
    if r_candidate is None:
        # 如果找不到满足 Delaunay 条件的 r，就找使得角 qpr 最大的 r
           max_angle = -1
           for r in S:
            if r == p or r == q:
                continue
            theta = angle(p, q, r)
            if theta > max_angle:
                max_angle = theta
                r_candidate = r  
           flag=False
    if r_candidate is None:
        raise ValueError(f"No valid clockwise edge found for {p}, {q}.")
    return r_candidate


def constant_workspace_delaunay(S: List[Point]) -> List[Tuple[Point, Point, Point]]:
    triangles = []
    global flag
    for pi in S:
        try:
            pj = first_delaunay_edge(pi, S)
        except ValueError:
            continue  # Skip this point if no valid first Delaunay edge is found

        j0 = pj
        while True:
            try:
                pk = clockwise_next_edge(pi, pj, S)
                if flag==True:
                   if S.index(pi) <S.index(pj) and S.index(pi) < S.index(pk):
                      triangles.append((pi, pj, pk))
                flag=True
                pj = pk
                if pj == j0:
                  break
            except ValueError:
                    break  # Exit the loop if no valid clockwise edge is found

    return triangles
def constant_workspace_delaunay_dummy(S: List[Point]) -> None:
    global flag
    for pi in S:
        try:
            pj = first_delaunay_edge(pi, S)
        except ValueError:
            continue

        j0 = pj
        while True:
            try:
                pk = clockwise_next_edge(pi, pj, S)
                # 👇 忽略输出，仅保留逻辑判断
                if flag:
                    if S.index(pi) < S.index(pj) and S.index(pi) < S.index(pk):
                        pass  # pretend to save (pi, pj, pk)
                flag = True
                pj = pk
                if pj == j0:
                    break
            except ValueError:
                break
