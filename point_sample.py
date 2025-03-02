import os
import re
import torch
from plyfile import PlyData, PlyElement
import numpy as np


def furthest_point_sampling(points,colors=None,semantics=None, n_samples=4096):
    """
    points: [N, 3] tensor containing the whole point cloud
    n_samples: samples you want in the sampled point cloud typically &lt;&lt; N 
    """
    # Convert points to PyTorch tensor if not already and move to GPU
    # print(colors)
    if(len(points)==0):
        return points,colors,semantics
    points = torch.Tensor(points).cuda()  # [N, 3]
    if colors is not None:
        colors=torch.Tensor(colors).cuda()
    if semantics is not None:
        semantics=torch.Tensor(semantics).cuda()

    # Number of points
    num_points = points.size(0)  # N

    # Initialize an array for the sampled indices
    sample_inds = torch.zeros(n_samples, dtype=torch.long).cuda()  # [S]

    # Initialize distances to inf
    dists = torch.ones(num_points).cuda() * float('inf')  # [N]

    # Select the first point randomly
    selected = torch.randint(num_points, (1,), dtype=torch.long).cuda()  # [1]
    sample_inds[0] = selected

    # Iteratively select points for a maximum of n_samples
    for i in range(1, n_samples):
        # Find the distance to the last added point in selected
        last_added = sample_inds[i - 1]  # Scalar
        dist_to_last_added_point = torch.sum((points[last_added] - points) ** 2, dim=-1)  # [N]

        # If closer, update distances
        dists = torch.min(dist_to_last_added_point, dists)  # [N]

        # Pick the one that has the largest distance to its nearest neighbor in the sampled set
        selected = torch.argmax(dists)  # Scalar
        sample_inds[i] = selected

    if colors is not None and semantics is not None:
        return points[sample_inds].cpu().numpy(),colors[sample_inds].cpu().numpy(), semantics[sample_inds].cpu().numpy() # [S, 3]
    elif colors is not None:
        return points[sample_inds].cpu().numpy(),colors[sample_inds].cpu().numpy()


# if __name__ == "__main__":
#     src_directory = 'error/pointcloud'

#     files = [f for f in os.listdir(src_directory) if f.startswith('pointcloud_') and f.endswith('.ply')]
        
#         # 提取前后数字并排序
#     files.sort(key=lambda x: (int(re.search(r'(\d+)\.ply$', x).group(1))))

#     for file in files:
#         ply_path = os.path.join(src_directory, file)

#         pc,colors = read_ply_with_colors(filename=ply_path)

