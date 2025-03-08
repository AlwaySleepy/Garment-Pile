"""
@date 2024/08/27
@content  train code
"""

import os
import sys
import torch
import torch.utils
import torch.utils.data
import fire
import numpy as np
import random
import matplotlib.pyplot as plt
import wandb

sys.path.append("Model_Train")
from config import opt  # 获取默认参数
from tqdm import tqdm
from torchnet import meter
from Model.pointnet2_Aff_Model import Aff_Model, Aff_Model_Loss
from Data_Utils.DataLoader_AffModel import DataLoader_AffModel
from Data_Utils.visualizer_utils import Visualize


def seed_eveything(seed=3407):
    """
    set seed
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def train(**kwargs):
    # update parameter according to terminal input
    opt.parse(kwargs)
    # create visualization window
    # vis = Visualize(opt.env)
    # set seed
    seed_eveything()
    # set wandb
    config = {
        "learning_rate": opt.lr,
        "epochs": opt.max_epoch,
        "batch_size": opt.batch_size,
        "optimizer": opt.optimizer,
    }
    wandb.init(
        project="Garment_PointNet2",
        name="Sofa_Model",
        config=config,
        resume="Sofa Model Version 0",
        # mode="online",
    )

    # ---------first step: load model---------#
    model = None
    # if path exists, loading the pre_trained model
    if opt.load_model_path:
        model = Aff_Model(normal_channel=False).cuda()
        model.load_state_dict(torch.load(opt.load_model_path))
        print("load model from %s" % opt.load_model_path)
    # else load new model
    else:
        model = Aff_Model(normal_channel=False).cuda()
        # init weight
        model.apply(weights_init)
    # push model to device
    model.to(opt.device)
    # use ReLU in-place, decrease use of GPU memory
    model.apply(inplace_relu)

    # ---------second step: load data---------#
    train_data = DataLoader_AffModel(mode="train", data_dir="Data/Sofa/Retrieve")
    val_data = DataLoader_AffModel(mode="val", data_dir="Data/Sofa/Retrieve")
    train_dataloader = torch.utils.data.DataLoader(
        dataset=train_data,
        batch_size=opt.batch_size,
        shuffle=True,
        num_workers=opt.num_workers,
    )
    val_dataloader = torch.utils.data.DataLoader(
        dataset=val_data,
        batch_size=opt.batch_size,
        shuffle=False,
        num_workers=opt.num_workers,
    )

    # ---------third step: define loss function and optimizer---------#
    # get criterion
    criterion = Aff_Model_Loss().cuda()
    # get optimizer
    if opt.optimizer == "Adam":
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=opt.lr,
            betas=opt.betas,
            eps=opt.eps,
            weight_decay=opt.weight_decay,
        )
    else:
        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=opt.lr,
            weight_decay=opt.weight_decay,
            momentum=opt.momentum,
        )

    # ---------fourth step: define evaluating indicator---------#
    # loss meter, store loss value of each batch and calculate the average value.
    loss_meter = meter.AverageValueMeter()
    # accurate meter, store loss value of each batch and calculate the average value.
    accurate_meter = meter.AverageValueMeter()
    # set previous loss to update lr later
    previous_loss = 1e20

    # ---------fifth step: train model---------#
    for epoch in range(opt.max_epoch):
        accurate_meter.reset()
        loss_meter.reset()
        # set status of neutral network to 'train'
        model.train()
        # history = {'train_loss':[], 'train_accuracy':[]}
        # set tqdm expression
        processbar = tqdm(
            train_dataloader, unit="step", total=len(train_dataloader), smoothing=0.9
        )
        for step, (data, label) in enumerate(processbar):
            data = data.to(opt.device)
            label = label.to(opt.device)
            # reset grad
            model.zero_grad()
            # print(data.shape)
            # input data to network
            output = model(data.transpose(2, 1))
            # calculate loss
            # print(output.shape, label.shape)
            loss = criterion(output, label)
            # update average meter
            loss_meter.add(loss.item())
            # inverse propagation
            loss.backward()
            # gradient optimization
            optimizer.step()

            # get accuracy
            pick_point_output = output[:, 0, :]
            # print("pick_point_output:", pick_point_output)
            prediction = (pick_point_output >= 0.5).float()
            # print("prediction:", prediction)
            correct = (prediction == label).sum().item()
            # print("correct:", correct)
            total = label.size(0)
            accuracy = correct / total
            # print("accuracy", accuracy)
            accurate_meter.add(accuracy)

            # draw picture in vis
            if (step + 1) % opt.print_freq == 0:
                # loss_meter.value() is (mean, std)
                # vis.plot('loss', loss_meter.value()[0])
                # vis.plot('accuracy', accurate_meter.value()[0])
                # history['train_loss'].append(loss_meter.value()[0])
                # history['train_accuracy'].append(accurate_meter.value()[0])
                # use wandb to print data
                wandb.log(
                    {
                        "loss": loss_meter.value()[0],
                        "accuracy": accurate_meter.value()[0],
                    }
                )

            # processbar output
            processbar.set_description(
                "[ TEST PART ][ %d / %d ], Loss:%.4f, accuracy:%.4f"
                % (
                    epoch + 1,
                    opt.max_epoch,
                    loss_meter.value()[0],
                    accurate_meter.value()[0],
                )
            )

        processbar.close()

        val_accuracy = val(model, val_dataloader)

        if (epoch + 1) % opt.print_freq == 0:
            # store model
            # torch.save(model, f"/home/isaac/PointNet2/Log/Two_Garment_Adhension_Model/Two_Garment_Adhension_Model_13000_{epoch+1}.pth")
            # store model_parameter
            # if dir not exists, create it
            if not os.path.exists("Model_Train/Model_Checkpoints/Sofa_Model"):
                os.makedirs("Model_Train/Model_Checkpoints/Sofa_Model")
            torch.save(
                model.state_dict(),
                f"Model_Train/Model_Checkpoints/Sofa_Model/Sofa_Model_Parameter_{epoch+1}.pth",
            )

        # update learning_rate
        if loss_meter.value()[0] > previous_loss:
            opt.lr = opt.lr * opt.lr_decay

        previous_loss = loss_meter.value()[0]

        wandb.log({"learning_rate": opt.lr, "val_accuracy": val_accuracy})


def inplace_relu(m):
    classname = m.__class__.__name__
    if classname.find("ReLU") != -1:
        m.inplace = True


def weights_init(m):
    classname = m.__class__.__name__
    if classname.find("Conv2d") != -1:
        torch.nn.init.xavier_normal_(m.weight.data)
        torch.nn.init.constant_(m.bias.data, 0.0)
    elif classname.find("Linear") != -1:
        torch.nn.init.xavier_normal_(m.weight.data)
        torch.nn.init.constant_(m.bias.data, 0.0)


@torch.no_grad()
def val(model, val_dataloader):
    """
    calculate accuracy in validation dataset.
    """
    # set model status to avoid grad forward
    model.eval()
    # set accuracy meter
    accurate_meter = meter.AverageValueMeter()
    accurate_meter.reset()
    # set processbar
    processbar = tqdm(
        val_dataloader, unit="step", total=len(val_dataloader), smoothing=0.9
    )
    # begin validation
    for step, (data, label) in enumerate(processbar):
        data = data.to(opt.device)
        label = label.to(opt.device)
        output = model(data.transpose(2, 1))
        # get accuracy
        pick_point_output = output[:, 0, :]
        # print("pick_point_output:", pick_point_output)
        prediction = (pick_point_output >= 0.5).float()
        # print("prediction:", prediction)
        correct = (prediction == label).sum().item()
        # print("correct:", correct)
        total = label.size(0)
        accuracy = correct / total
        # print("accuracy", accuracy)
        accurate_meter.add(accuracy)

        processbar.set_description(
            "[ VAL PART ], accuracy:%.4f" % (accurate_meter.value()[0])
        )

    # set model status to 'train'
    model.train()
    # return accuracy
    return accurate_meter.value()[0]


if __name__ == "__main__":

    train()
