import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

def read_data(file_path, grid_resolution=100):
    """
    讀取 CSV 數據並對所有參數欄位進行插值。
    
    Parameters:
    -----------
    file_path : str
        CSV 檔案路徑
    grid_resolution : int
        插值網格的解析度（預設：100）
        
    Returns:
    --------
    tuple
        (z_mesh_dict, r_mesh, theta_mesh)
        - z_mesh_dict: 字典，鍵為欄位名稱，值為插值後的 z_mesh
        - r_mesh: 半徑網格
        - theta_mesh: 角度網格
    """
    # 讀取 CSV 檔案
    df = pd.read_csv(file_path)
    
    # 提取半徑和角度數據
    radius = df.iloc[:, 0].values  # 第一欄：半徑
    angle = df.iloc[:, 1].values    # 第二欄：角度
    
    # 將角度轉換為弧度
    angle_rad = np.radians(angle)
    
    # 創建插值網格
    r_min, r_max = radius.min(), radius.max()
    # 增加一點邊界以確保覆蓋所有數據點
    r_buffer = (r_max - r_min) * 0.05
    r_grid = np.linspace(r_min - r_buffer, r_max + r_buffer, grid_resolution)
    theta_grid = np.linspace(np.radians(0), np.radians(90), grid_resolution)
    
    # 創建網格
    r_mesh, theta_mesh = np.meshgrid(r_grid, theta_grid)
    
    # 轉換為笛卡爾座標進行插值
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    x_mesh = r_mesh * np.cos(theta_mesh)
    y_mesh = r_mesh * np.sin(theta_mesh)
    
    # 從第三欄開始都是參數數據
    param_columns = df.columns.tolist()[2:]
    
    # 創建結果字典
    z_mesh_dict = {}
    
    # 對每個參數進行插值
    for col in param_columns:
        intensity = df[col].values
        # 使用 cubic 插值，如果失敗則使用 linear
        try:
            z_mesh = griddata((x, y), intensity, (x_mesh, y_mesh), method='cubic')
        except:
            z_mesh = griddata((x, y), intensity, (x_mesh, y_mesh), method='linear')
        
        # 填充 NaN 值（使用最近鄰插值）
        mask = np.isnan(z_mesh)
        if mask.any():
            z_mesh_nearest = griddata((x, y), intensity, (x_mesh, y_mesh), method='nearest')
            z_mesh[mask] = z_mesh_nearest[mask]
        
        z_mesh_dict[col] = z_mesh
    
    return z_mesh_dict, r_mesh, theta_mesh

def plot_polar_heatmap(z_mesh_dict, r_mesh, theta_mesh, val_min=None, val_max=None, 
                      cmap='viridis', figsize=None, save_path=None, dpi=300):
    """
    繪製極坐標熱圖。
    
    Parameters:
    -----------
    z_mesh_dict : dict
        參數名稱與 z_mesh 陣列的字典
    r_mesh : array
        半徑網格
    theta_mesh : array
        角度網格
    val_min : float
        色彩標尺的最小值（預設：自動計算）
    val_max : float
        色彩標尺的最大值（預設：自動計算）
    cmap : str or Colormap
        色彩映射（預設：'viridis'）
    figsize : tuple
        圖形大小（預設：根據參數數量自動計算）
    save_path : str
        儲存路徑（預設：None，不儲存）
    dpi : int
        儲存圖片的解析度（預設：300）
    """
    n_params = len(z_mesh_dict)
    
    # 自動計算數值範圍
    if val_min is None or val_max is None:
        all_values = []
        for z_mesh in z_mesh_dict.values():
            all_values.extend(z_mesh[~np.isnan(z_mesh)].flatten())
        if val_min is None:
            val_min = np.percentile(all_values, 1)  # 使用百分位數避免極端值
        if val_max is None:
            val_max = np.percentile(all_values, 99)
    
    # 自動計算圖形大小
    if figsize is None:
        if n_params == 1:
            figsize = (10, 10)
        elif n_params == 2:
            figsize = (16, 8)
        else:
            figsize = (min(8 * n_params, 24), 8)
    
    # 創建圖形
    fig = plt.figure(figsize=figsize)
    
    if n_params == 1:
        axes = [fig.add_subplot(111, projection='polar')]
    else:
        axes = []
        for i in range(n_params):
            ax = fig.add_subplot(1, n_params, i+1, projection='polar')
            axes.append(ax)
    
    # 繪製每個參數
    for idx, (param_name, z_mesh) in enumerate(z_mesh_dict.items()):
        ax = axes[idx]
        
        # 繪製熱圖
        c = ax.pcolormesh(theta_mesh, r_mesh, z_mesh, cmap=cmap, 
                         shading='gouraud',  # 使用 gouraud 使顏色更平滑
                         vmin=val_min, vmax=val_max)
        
        # 設定角度方向和零點位置
        ax.set_theta_direction(1)  # 逆時針
        ax.set_theta_zero_location('S')  # 南方為 0°
        
        # 設定可見範圍（0° 到 90°）
        ax.set_thetamin(0)
        ax.set_thetamax(90)
        
        # 添加色彩條
        cbar = plt.colorbar(c, ax=ax, pad=0.1, shrink=0.8)
        cbar.set_label(f'Intensity', rotation=270, labelpad=20)
        cbar.ax.tick_params(labelsize=10)
        
        # 設定標籤
        ax.set_xlabel('Radius (nm)', labelpad=30, fontsize=12)
        ax.set_title(f'{param_name}', pad=20, fontsize=14, fontweight='bold')
        
        # 自定義角度標籤
        theta_positions = np.array([0, 30, 60, 90])
        theta_labels = ['0°', '30°', '60°', '90°']
        ax.set_thetagrids(theta_positions, labels=theta_labels, fontsize=11)
        
        # 設定半徑標籤
        ax.tick_params(axis='y', labelsize=10)
        
        # 添加網格
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 設定背景顏色
        ax.set_facecolor('#f8f8f8')
    
    # 調整佈局
    plt.tight_layout()
    
    # 添加總標題（如果有多個參數）
    if n_params > 1:
        fig.suptitle('Polar Heatmap Visualization', fontsize=16, y=1.02)
    
    # 儲存圖形
    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight', facecolor='white')
        print(f"圖形已儲存至: {save_path}")
    
    return fig

def analyze_data(z_mesh_dict):
    """
    分析數據並印出統計資訊。
    
    Parameters:
    -----------
    z_mesh_dict : dict
        參數名稱與 z_mesh 陣列的字典
    """
    print("\n=== 數據分析結果 ===")
    print(f"參數數量: {len(z_mesh_dict)}")
    print("\n各參數統計資訊:")
    
    for param_name, z_mesh in z_mesh_dict.items():
        valid_data = z_mesh[~np.isnan(z_mesh)]
        print(f"\n{param_name}:")
        print(f"  最小值: {valid_data.min():.3f}")
        print(f"  最大值: {valid_data.max():.3f}")
        print(f"  平均值: {valid_data.mean():.3f}")
        print(f"  標準差: {valid_data.std():.3f}")
        print(f"  中位數: {np.median(valid_data):.3f}")

# 主程式
if __name__ == "__main__":
    # 設定檔案路徑
    file_path = r'C:\Users\renfo\Downloads\Tilt angle.csv'
    
    # 讀取並插值數據
    print("正在讀取並處理數據...")
    z_mesh_dict, r_mesh, theta_mesh = read_data(file_path, grid_resolution=150)
    
    # 分析數據
    analyze_data(z_mesh_dict)
    
    # 繪製熱圖
    print("\n正在繪製熱圖...")
    fig = plot_polar_heatmap(
        z_mesh_dict, 
        r_mesh, 
        theta_mesh,
        val_min=0,      # 可以設為 None 以自動計算
        val_max=12,     # 可以設為 None 以自動計算
        cmap='viridis',
        save_path='polar_heatmap_optimized.png'  # 可選：儲存圖片
    )
    
    # 顯示圖形
    plt.show()
    
    # 也可以嘗試其他色彩映射
    # 例如：'plasma', 'inferno', 'magma', 'cividis', 'turbo', 'RdBu_r', 'coolwarm'