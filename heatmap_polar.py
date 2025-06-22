import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def ReadData(filePath):
    """
    Read CSV data and interpolate for all parameter columns.
    
    Parameters:
    -----------
    filePath : str
        Path to the CSV file
        
    Returns:
    --------
    dict
        Dictionary with column names as keys and interpolated z_mesh as values
    """
    # Read the CSV file
    df = pd.read_csv(filePath)
    
    # Extract radius and angle data
    radius = df['Radius (nm)'].values
    angle = df['Angle (deg.)'].values
    
    # Convert angles to radians
    angle_rad = np.radians(angle)
    
    # Create interpolation grid for quarter circle
    r_min, r_max = radius.min(), radius.max()
    r_grid = np.linspace(r_min, r_max, 100)
    # From 270° to 180° in standard polar coordinates
    theta_grid = np.linspace(np.radians(0), np.radians(90), 100)
    
    # Create mesh grid
    r_mesh, theta_mesh = np.meshgrid(r_grid, theta_grid)
    
    # Convert to cartesian for interpolation
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    x_mesh = r_mesh * np.cos(theta_mesh)
    y_mesh = r_mesh * np.sin(theta_mesh)
    
    # Find all parameter columns (columns that start with #)
    param_columns = [col for col in df.columns if col.startswith('#')]
    
    # Create result dictionary
    z_mesh_dict = {}
    
    # Interpolate each parameter
    for col in param_columns:
        intensity = df[col].values
        z_mesh = griddata((x, y), intensity, (x_mesh, y_mesh), method='cubic')
        z_mesh_dict[col] = z_mesh
    
    return z_mesh_dict

def plot_polar_heatmap(z_mesh_dict, ValMin, ValMax, cmap='viridis', figsize=None):
    """
    Plot polar heatmaps based on the number of parameters.
    
    Parameters:
    -----------
    z_mesh_dict : dict
        Dictionary with parameter names as keys and z_mesh arrays as values
    ValMin : float
        Minimum value for color scale normalization
    ValMax : float
        Maximum value for color scale normalization
    cmap : str
        Colormap name (default: 'viridis')
    figsize : tuple
        Figure size (default: auto-calculated based on number of parameters)
    """
    n_params = len(z_mesh_dict)
    
    # Auto-calculate figure size if not provided
    if figsize is None:
        if n_params == 1:
            figsize = (10, 10)
        else:
            figsize = (8 * n_params, 8)
    
    # Create figure
    if n_params == 1:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='polar')
        axes = [ax]
    else:
        fig = plt.figure(figsize=figsize)
        axes = []
        for i in range(n_params):
            ax = fig.add_subplot(1, n_params, i+1, projection='polar')
            axes.append(ax)
    
    # Create grid for plotting (same as in ReadData)
    r_grid = np.linspace(-5, 10, 100)  # Adjust based on your data range
    theta_grid = np.linspace(np.radians(0), np.radians(90), 100)
    r_mesh, theta_mesh = np.meshgrid(r_grid, theta_grid)
    
    # Plot each parameter
    for idx, (param_name, z_mesh) in enumerate(z_mesh_dict.items()):
        ax = axes[idx]
        
        # Plot the heatmap with normalized color scale
        c = ax.pcolormesh(theta_mesh, r_mesh, z_mesh, cmap=cmap, shading='auto', 
                         vmin=ValMin, vmax=ValMax)
        
        # Set theta direction and zero location
        ax.set_theta_direction(1)  # Counterclockwise
        ax.set_theta_zero_location('S')  # South at 0°
        
        # Set visible range (0° to 90° )
        ax.set_thetamin(0)
        ax.set_thetamax(90)
        
        # Add colorbar
        cbar = plt.colorbar(c, ax=ax, pad=0.1)
        cbar.set_label(f'Intensity ({param_name})', rotation=270, labelpad=20)
        
        # Set labels
        ax.set_xlabel('Radius (nm)', labelpad=30)
        ax.set_title(f'Polar Heatmap of {param_name}', pad=20)
        
        # Customize theta labels to show 0° at south, 90° at east
        # 270° in standard = 0° in our system
        # 180° in standard = 90° in our system
        theta_positions = np.array([0, 30, 60, 90])  # Standard polar positions
        theta_labels = ['0°', '30°', '60°', '90°']  # Our labels
        ax.set_thetagrids(theta_positions, labels=theta_labels)
        
        # Add grid
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Main execution
if __name__ == "__main__":
    # Set file path
    file_path = r'C:\Users\renfo\Downloads\Tilt angle.csv'
    
    # Read and interpolate data
    z_mesh_dict = ReadData(file_path)
    
    # Plot the heatmap(s) with normalized intensity range 0-15
    fig = plot_polar_heatmap(z_mesh_dict, ValMin=0, ValMax=12, cmap='viridis')
    
    # Show the plot
    plt.show()
    
    # Optional: Save the figure
    # fig.savefig('polar_heatmap.png', dpi=300, bbox_inches='tight')