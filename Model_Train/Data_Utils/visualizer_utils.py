import visdom
import time
import numpy as np

class Visualize(object):
    #object是一个最普通的基类，创建类时默认从object基类派生
    '''
    封装了visdom的基本操作
    @仍然可以通过`self.vis.function`或者`self.function`调用原生的visdom接口
    @比如
    @self.text('hello visdom')
    @self.histogram(t.randn(1000))
    @self.line(t.arange(0, 10),t.arange(1, 11))
    '''

    def __init__(self, env='default', **kwargs):
        '''
        env表示visdom的环境参数;

        此函数用于初始化visdom
        '''
        #通过指定不同的环境名称，可以在 Visdom 服务器中创建多个独立的可视化窗口，以便对不同的实验或数据进行可视化和比较。
        self.vis = visdom.Visdom(env=env, **kwargs)
        #用于存储横坐标相关信息（字典的形式）
        self.index = {}
        self.log_text = ''

    def reinit(self, env='default', **kwargs):
        '''
        env表示visdom的环境参数;

        此函数用于修改visdom的配置
        '''
        self.vis = visdom.Visdom(env, **kwargs)
        return self

    def plot(self, name, y, **kwargs):
        '''
        name表示图表的名称;

        y表示要绘制的数据点的纵坐标;

        **kwargs表示任意数量的关键字参数;

        该函数用于在 Visdom 中绘制线性图


        示例 : self.plot('loss', 1.00)
        '''
        #获取存储在 self.index 字典中以 name 为键的值，如果该键不存在，则返回默认值 0
        #这个值通常用于表示当前 name 对应的数据点的横坐标位置
        x = self.index.get(name, 0)
        #使用 Visdom 的 line 方法绘制线性图
        self.vis.line(Y=np.array([y]),      #表示纵坐标的值，使用了 NumPy 数组包装 y
                      X=np.array([x]),      #表示横坐标的值，使用了 NumPy 数组包装 x
                      win=(name),           #表示图表的名称
                      opts=dict(title=name),    #表示图表的标题，这里使用与名称相同的字符串作为标题
                      update=None if x == 0 else 'append',      #表示更新图表的模式，如果 x 为 0，则表示新建图表，否则表示追加数据到已有图表。
                      **kwargs )
        self.index[name] = x + 1            #用于更新 self.index 字典中以 name 为键的值，将其加 1，以表示下一个数据点的横坐标位置。

    def img(self, name, img_, **kwargs):
        '''
        @param name表示图像名称
        @param img_表示要显示的图像数据
        @param **kwargs表示任意数量的关键字
        @discription 该函数用于在 Visdom 中显示图像
        @example self.img('input_img', t.Tensor(64, 64))
        @example self.img('input_imgs', t.Tensor(100, 3, 64, 64), nrows=10)
        '''
        self.vis.images(#Visdom 接受的图像数据需要是 NumPy 数组格式，且NumPy 不支持 GPU 上的张量；
                        img_.cpu().numpy(),     #将张量从 GPU 上转移到 CPU 上，然后转换为 NumPy 数组
                        win=(name),             #表示图像的名称
                        opts=dict(title=name),  #表示图像的标题，这里使用与名称相同的字符串作为标题
                        **kwargs )

    def plot_many(self, d):
        '''
        @params d: dict (name, value) i.e. ('loss', 0.11)
        @discription 一次plot多个
        '''
        for k, v in d.items():
            self.plot(k, v)

    def img_many(self, d):
        '''
        一次img多个
        @params d: dict (name, img_value) i.e. ('loss', XXX)
        '''
        for k, v in d.items():
            self.img(k, v)

    def log(self, info, win='log_text'):
        '''
        @param info:表示要记录的日志信息，可以是字符串或字典形式
        @param win:表示用于显示日志信息的窗口名称，默认为 'log_text'
        @example self.log({'loss':1, 'lr':0.0001})
        '''
        self.log_text += ('[{time}] {info} <br>'.format(
                            time=time.strftime('%m%d_%H%M%S'),
                            info=info))             #将新的日志信息追加到 self.log_text 字符串变量
        self.vis.text(self.log_text, win)           #将日志信息显示在指定的窗口中

    def __getattr__(self, name):
        '''
        自定义的plot,image,log,plot_many等除外
        self.function 等价于self.vis.function
        '''
        return getattr(self.vis, name)
