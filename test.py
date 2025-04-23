import matplotlib.pyplot as plt
import random
import time
import sys
import gc
import numpy as np
import tracemalloc
from incremental import incremental_delaunay_dummy
from constant import constant_workspace_delaunay_dummy

Point = tuple[float, float]
def estimate_memory(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, (list, tuple)):
        size += sum(estimate_memory(o) for o in obj)
    return size

def generate_general_position_points(n: int, bound: float = 100.0, delta: float = 1e-3) -> list[Point]:
    def is_cocircular(a, b, c, d) -> bool:
        mat = [
            [a[0], a[1], a[0]**2 + a[1]**2, 1],
            [b[0], b[1], b[0]**2 + b[1]**2, 1],
            [c[0], c[1], c[0]**2 + c[1]**2, 1],
            [d[0], d[1], d[0]**2 + d[1]**2, 1],
        ]
        return abs(np.linalg.det(mat)) < 1e-6

    points = []
    attempts = 0
    while len(points) < n and attempts < 10000:
        x = random.uniform(0, bound) + random.uniform(-delta, delta)
        y = random.uniform(0, bound) + random.uniform(-delta, delta)
        candidate = (round(x, 6), round(y, 6))
        valid = True
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                for k in range(j + 1, len(points)):
                    if is_cocircular(points[i], points[j], points[k], candidate):
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                break
        if valid:
            points.append(candidate)
        attempts += 1
    return points

def draw_triangulation(points, triangles, title="Triangulation"):
    plt.figure()
    for tri in triangles:
        poly = list(tri) + [tri[0]]
        xs, ys = zip(*poly)
        plt.plot(xs, ys, 'k-')
    px, py = zip(*points)
    plt.plot(px, py, 'ro', markersize=4)
    plt.title(title)
    plt.axis('equal')
    plt.grid(True)

if __name__ == "__main__":
    '''#points=generate_general_position_points(50)
    #points=[(41.272132, 13.10693), (41.109134, 17.936294), (21.684912, 58.625498), (2.20814, 12.288039), (13.039992, 19.989059)]
    #points = [(94.2219, 78.570962),(91.005163, 38.717717),(2.854946, 91.85847)]
    #points = [(41.48058, -69.065055),(100, 100),(31.86846, 99.642031),(77.15, -24)]
    #Iconstant
    tracemalloc.start()
    start_const = time.time()
    tris_const = constant_workspace_delaunay(points)
    end_const = time.time()
    current_cosnt, peak_const = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    output_size=estimate_memory(tris_const)
    workspace=peak_const-output_size

    # #Incremental
    tracemalloc.start()
    start_inc = time.time()
    tris_inc = incremental_delaunay_optimized(points)
    end_inc = time.time()
    current_inc, peak_inc = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"[Incremental]  Time: {end_inc - start_inc:.6f}s, Peak Memory: {peak_inc / 1024:.2f} KB")
    #print(f"[Constant Workspace] Triangles: {len(tris_const)}, Time: {end_const - start_const:.6f}s, Peak Memory: {workspace / 1024:.2f} KB")

    draw_triangulation(points, tris_inc, "Incremental Delaunay")
    #draw_triangulation(points, tris_const, "Constant Workspace Delaunay")
    plt.show()'''

# 用于存储数据
# 用于存储数据
# 用于存储数据
n_values = [10, 20, 30,40,50,60,70, 80,90, 100,120,140,160,180,200,250,300,350,400,450,500]
time_const_mean = []

time_inc_mean = []

mem_const_mean = []

mem_inc_mean = []


# 重复次数
num_trials = 5

# 进行比较
for n in n_values:
    time_cons_trials = []
    mem_cons_trials = []
    time_inc_trials = []
    mem_inc_trials = []
    
    for _ in range(num_trials):
        points = generate_general_position_points(n)

        # 测量 constant_workspace_delaunay_dummy
        tracemalloc.start()
        start_cons = time.time()
        constant_workspace_delaunay_dummy(points)
        end_cons = time.time()
        current_cons, peak_cons = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 记录测量结果
        time_cons_trials.append(end_cons - start_cons)
        mem_cons_trials.append(peak_cons / 1024)  # 转换为KB

        # 测量 incremental_delaunay_dummy
        tracemalloc.start()
        start_inc = time.time()
        incremental_delaunay_dummy(points)
        end_inc = time.time()
        current_inc, peak_inc = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 记录测量结果
        time_inc_trials.append(end_inc - start_inc)
        mem_inc_trials.append(peak_inc / 1024)  # 转换为KB

    # 计算平均值和标准差
    time_const_mean.append(np.mean(time_cons_trials))
    mem_const_mean.append(np.mean(mem_cons_trials))
    
    time_inc_mean.append(np.mean(time_inc_trials))
    mem_inc_mean.append(np.mean(mem_inc_trials))
    # 输出结果
    print(f"n={n:>5} | Time (constant): {time_const_mean[-1]:.4f}s | Peak Mem (constant): {mem_const_mean[-1]:.2f} KB ")
    print(f"n={n:>5} | Time (incremental): {time_inc_mean[-1]:.4f}s | Peak Mem (incremental): {mem_inc_mean[-1]:.2f} KB")

# 绘制时间对比图
plt.figure(figsize=(12, 6))

# 时间比较图
plt.subplot(1, 2, 1)
plt.errorbar(n_values, time_const_mean, label="Constant Algorithm", fmt='o', color='b', capsize=5)
plt.errorbar(n_values, time_inc_mean,label="Incremental Algorithm", fmt='o', color='r', capsize=5)
plt.xlabel('Number of Points (n)')
plt.ylabel('Time (s)')
plt.title('Execution Time Comparison with Standard Deviation')
plt.legend()

# 内存比较图
plt.subplot(1, 2, 2)
plt.errorbar(n_values, mem_const_mean, label="Constant Algorithm", fmt='o', color='b', capsize=5)
plt.errorbar(n_values, mem_inc_mean, label="Incremental Algorithm", fmt='o', color='r', capsize=5)
plt.xlabel('Number of Points (n)')
plt.ylabel('Peak Memory (KB)')
plt.title('Peak Memory Comparison with Standard Deviation')
plt.legend()

# 显示图表
plt.tight_layout()
plt.show()