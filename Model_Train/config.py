"""
@author wyr
@date 2024/05/25
@content 配置文件，所有可配置的变量都集中于此，并提供默认值
"""

import warnings
import torch


class DefaultConfig(object):

    load_model_path = None  # 加载与训练模型的路径，为None表示不加载

    batch_size = 128  # batch size_128
    use_gpu = True  # 是否使用GPU
    num_workers = 12  # 加载数据时使用多少个工作单位_8
    print_freq = 5  # 每N个batch打印一次信息_4

    optimizer = "Adam"  # Adam or SGD
    max_epoch = 80  # 训练轮数_80
    lr = 0.0008  # 初始化学习率
    lr_decay = 0.95  # 学习率衰减，lr = lr * lr_decay，随着训练的进行逐渐减小学习率的大小，使得模型在训练后期更容易收敛到全局最优解而不是在最优解附近振荡
    weight_decay = 1e-4  # 权重衰减，一种正则化技术，通过向损失函数添加一个惩罚项来减小模型的权重值，以防止过拟合，提高模型的泛化能力
    betas = (0.9, 0.999)  # 两个超参数，分别控制一阶和二阶矩估计的指数衰减率。
    eps = 1e-08  # 用于数值稳定性的小常数。它在计算更新时用于防止除以零的错误。
    momentum = 0.9  # 动量因子。动量可以加速 SGD 在相关方向上的收敛，并减少震荡。通常设置在 0 和 1 之间。

    def parse(self, kwargs):
        """
        根据字典kwargs 更新 config参数
        @使用示例
        @opt = DefaultConfig()
        @new_config = {'lr':0.1, 'use_gpu':False}
        @opt.parse(new_config)
        """
        # 更新配置参数
        for k, v in kwargs.items():
            if not hasattr(self, k):
                warnings.warn("Warning: opt has not attribute %s" % k)
            setattr(self, k, v)

        opt.device = torch.device("cuda") if opt.use_gpu else torch.device("cpu")

        # 打印配置信息
        print("user config:")
        for k, v in self.__class__.__dict__.items():
            if not k.startswith("_"):
                print(k, getattr(self, k))


opt = DefaultConfig()
