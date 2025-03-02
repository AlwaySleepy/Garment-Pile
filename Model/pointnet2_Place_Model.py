import torch
import torch.nn as nn
import torch.nn.functional as F

from Model.pointnet2_utils import PointNetSetAbstractionMsg, PointNetSetAbstraction, PointNetFeaturePropagation

class Place_Model(nn.Module):
    def __init__(self, normal_channel=False):
        super(Place_Model, self).__init__()
        if normal_channel:
            additional_channel = 3
        else:
            additional_channel = 0
        self.normal_channel = normal_channel

        self.sa1_pick = PointNetSetAbstraction(npoint=512, radius=0.2, nsample=32, in_channel=6+additional_channel, mlp=[64, 64, 128], group_all=False)
        self.sa2_pick = PointNetSetAbstraction(npoint=128, radius=0.4, nsample=64, in_channel=128 + 3, mlp=[128, 128, 256], group_all=False)
        self.sa3_pick = PointNetSetAbstraction(npoint=None, radius=None, nsample=None, in_channel=256 + 3, mlp=[256, 512, 1024], group_all=True)
        self.fp3_pick = PointNetFeaturePropagation(in_channel=1280, mlp=[256, 256])
        self.fp2_pick = PointNetFeaturePropagation(in_channel=384, mlp=[256, 128])
        self.fp1_pick = PointNetFeaturePropagation(in_channel=128+6+additional_channel, mlp=[128, 128, 128])

        self.sa1_place = PointNetSetAbstraction(npoint=512, radius=0.2, nsample=32, in_channel=6+additional_channel, mlp=[64, 64, 128], group_all=False)
        self.sa2_place = PointNetSetAbstraction(npoint=128, radius=0.4, nsample=64, in_channel=128 + 3, mlp=[128, 128, 256], group_all=False)
        self.sa3_place = PointNetSetAbstraction(npoint=None, radius=None, nsample=None, in_channel=256 + 3, mlp=[256, 512, 1024], group_all=True)
        self.fp3_place = PointNetFeaturePropagation(in_channel=1280, mlp=[256, 256])
        self.fp2_place = PointNetFeaturePropagation(in_channel=384, mlp=[256, 128])
        self.fp1_place = PointNetFeaturePropagation(in_channel=128+6+additional_channel, mlp=[128, 128, 128])

        self.conv1 = nn.Conv1d(256, 128, 1)
        self.bn1 = nn.BatchNorm1d(128)
        self.drop1 = nn.Dropout(0.5)
        self.conv2 = nn.Conv1d(128, 1, 1)


    def forward(self, xyz_pick, xyz_place):
        assert xyz_pick.shape == xyz_place.shape
        B,C,N = xyz_pick.shape
        # Set Pick
        if self.normal_channel:
            l0_points_pick = xyz_pick
            l0_xyz_pick = xyz_pick[:,:3,:]
        else:
            l0_points_pick = xyz_pick
            l0_xyz_pick = xyz_pick
        # Pick Abstraction Layers
        l1_xyz_pick, l1_points_pick = self.sa1_pick(l0_xyz_pick, l0_points_pick)
        l2_xyz_pick, l2_points_pick = self.sa2_pick(l1_xyz_pick, l1_points_pick)
        l3_xyz_pick, l3_points_pick = self.sa3_pick(l2_xyz_pick, l2_points_pick)
        # Pick Feature Propagation Layers
        l2_points_pick = self.fp3_pick(l2_xyz_pick, l3_xyz_pick, l2_points_pick, l3_points_pick)
        l1_points_pick = self.fp2_pick(l1_xyz_pick, l2_xyz_pick, l1_points_pick, l2_points_pick)
        l0_points_pick = self.fp1_pick(l0_xyz_pick, l1_xyz_pick, torch.cat([l0_xyz_pick,l0_points_pick],1), l1_points_pick)

        # Set Place
        if self.normal_channel:
            l0_points_place = xyz_place
            l0_xyz_place = xyz_place[:,:3,:]
        else:
            l0_points_place = xyz_place
            l0_xyz_place = xyz_place
        # Place Abstraction Layers
        l1_xyz_place, l1_points_place = self.sa1_place(l0_xyz_place, l0_points_place)
        l2_xyz_place, l2_points_place = self.sa2_place(l1_xyz_place, l1_points_place)
        l3_xyz_place, l3_points_place = self.sa3_place(l2_xyz_place, l2_points_place)
        # Place Feature Propagation Layers
        l2_points_place = self.fp3_place(l2_xyz_place, l3_xyz_place, l2_points_place, l3_points_place)
        l1_points_place = self.fp2_place(l1_xyz_place, l2_xyz_place, l1_points_place, l2_points_place)
        l0_points_place = self.fp1_place(l0_xyz_place, l1_xyz_place, torch.cat([l0_xyz_place,l0_points_place],1), l1_points_place)

        pick_feature = l0_points_pick[:, :, 0]
        pick_feature_expanded = pick_feature.unsqueeze(2).repeat(1, 1, 4096)
        mixed_feature = torch.cat((pick_feature_expanded, l0_points_place), 1)

        # FC layers
        feat = F.relu(self.bn1(self.conv1(mixed_feature)))
        output = self.drop1(feat)
        output = self.conv2(output)
        output = torch.sigmoid(output)
        output = output.permute(0, 2, 1)
        
        return output


# model = Place_Model(normal_channel=False)

# B, C, N = 8, 3, 4096
# xyz_pick = torch.rand(B, C, N)
# xyz_place = torch.rand(B, C, N)

# output = model(xyz_pick, xyz_place)

# # 打印结果形状
# print(f"mixed_feature shape: {output.shape}")

class Place_Model_Loss(nn.Module):

    def __init__(self):

        super(Place_Model_Loss, self).__init__()

    def forward(self, pred, target):
        '''
        Args:
        - pred : (B, N, 1)  ->  prediction output of model.
        - target : (B, 1)   ->  target value.

        Loss Function : 
        - binary_cross_entropy

        Output:
        - loss
        '''
        # get shape parameter.
        B, N, _ = pred.shape   
        # shape of 'pred_selected' is (B,), indicating the probability of chosen point.
        pred_selected = pred[torch.arange(B), 0, 0]  
        # print("prediction_probability is ", pred_selected)
        # change the shape of target from (B, 1) to (B,)
        target = target.view(-1)
        # use binary cross entropy to calculate loss.
        loss = F.binary_cross_entropy(pred_selected, target)

        return loss