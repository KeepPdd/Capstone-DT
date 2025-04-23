import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 读取数据
df_c = pd.read_csv("Constant.csv")
df_i = pd.read_csv("Incremental.csv")

n_c, t_c, m_c = df_c["n"], df_c["Time (s)"], df_c["Peak Mem (KB)"]
n_i, t_i, m_i = df_i["n"], df_i["Time (s)"], df_i["Peak Mem (KB)"]

# 定义拟合模型函数
def model_on2(n, a):       # O(n^2)
    return a * n**2

def model_onlogn(n, a):    # O(n log n)
    return a * n * np.log2(n)

def model_on(n, a):        # O(n)
    return a * n

# 拟合时间复杂度
a_on2, _ = curve_fit(model_on2, n_c, t_c)
a_onlogn, _ = curve_fit(model_onlogn, n_i, t_i)

# 拟合内存复杂度
a_mem_on, _ = curve_fit(model_on, n_i, m_i)

# 生成平滑 x 轴用于画拟合曲线
n_fit = np.linspace(min(n_c.min(), n_i.min()), max(n_c.max(), n_i.max()), 300)

# -------------------------------
# 图 1：运行时间 vs 输入规模 n
# -------------------------------
plt.figure(figsize=(10, 6))
plt.plot(n_c, t_c, 'o-', label='Constant - Time')
plt.plot(n_i, t_i, 's-', label='Incremental - Time')

plt.plot(n_fit, model_on2(n_fit, *a_on2), 'k--', label=r'Fitted $O(n^2)$ (Constant)')
plt.plot(n_fit, model_onlogn(n_fit, *a_onlogn), 'g--', label=r'Fitted $O(n \log n)$ (Incremental)')

plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.title("Runtime vs Input Size with Complexity Fitting")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------
# 图 2：内存使用 vs 输入规模 n
# -------------------------------
plt.figure(figsize=(10, 6))
plt.plot(n_c, m_c, 'o-', label='Constant - Memory')
plt.plot(n_i, m_i, 's-', label='Incremental - Memory')

plt.axhline(np.mean(m_c), color='k', linestyle='--', label=r'Fitted $O(1)$ (Constant)')
plt.plot(n_fit, model_on(n_fit, *a_mem_on), 'g--', label=r'Fitted $O(n)$ (Incremental)')

plt.xlabel("Input Size (n)")
plt.ylabel("Memory Usage (KB)")
plt.title("Memory Usage vs Input Size with Complexity Fitting")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

