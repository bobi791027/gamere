#gamere:一个Python3.8的游戏第三方库
##什么是gamere?
gamere基于**pygame**，适合开发方格类的二维游戏

##安装gamere
```cmd
git clone https://github.com/bobi791027/gamere
python -m pip install -r requirement.txt
python setup.py install
```

##gamere的优点
以下代码实现的**黑白迭代**小游戏，仅用了**71**行代码
```python
import gamere as cpp
import pygame
import random

flatten = lambda L: sum(map(TyFlatten, L), []) if isinstance(L, list) else [L]

def reverse(lay, pos):
    row, column = pos
    if row < 0 or column < 0:
        return lay
    try:
        if lay[row][column] == black:
            lay[row][column] = white
        else:
            lay[row][column] = black
    except IndexError:
        pass
    finally:
        return lay


def move(row, column, lay):
    reverse(lay, (row, column))
    reverse(lay, (row + 1, column))
    reverse(lay, (row - 1, column))
    reverse(lay, (row, column + 1))
    reverse(lay, (row, column - 1))
    return lay


def handler(event):
    if event.type == cpp.MOUSEBUTTONDOWN:
        x, y = event.pos
        row, column = x // 40, y // 40
        if row < 0 or row >= gamewidth or column < 0 or column >= gamewidth:
            return
        lay = layout.layout
        layout.layout = move(row, column, lay)


def update():
    text = font.render(f'TIMER: {timer.timer()}', True, (0, 0, 0))
    window.screen.blit(text, (gamewidth * 40 + 1, window.height // 2))
    if black not in flatten(layout.layout):
        window.running = False


def last():
    window = cpp.Window(background='resources/background.bmp', title='作答成功', size=(300, 300))
    text = cpp.Text('resources/fonts/alpha.ttf', window, size=45, text=f'Okay,Timer {timer.timer()}')
    window.loop(update=text.update)


black = cpp.Image('resources/black.bmp')
white = cpp.Image('resources/white.bmp')
gamewidth = 15
timer = cpp.Timer()
font = pygame.font.Font('resources/fonts/alpha.ttf', 20)
mapping = [[white for i in range(gamewidth)] for j in range(gamewidth)]
for i in range(45):
    mapping = move(random.randint(0, gamewidth - 1), random.randint(0, gamewidth - 1), mapping)
layout = cpp.Layout(mapping)
window = cpp.Window('resources/background.bmp', title='黑白迭代', size=(gamewidth * 40 + 100, gamewidth * 40))
layout.loop(window, draw=True, handler=handler, update=update, last=last)
```

##gamere使用
###init
初始化gamere
```python
init(**kwargs)
```

###GamereError
gamere的错误类型

###GamereWarning
gamere的警告类型

###Window
gamere窗口主题
####init
```python
Window(background='',  # 背景图片路径，寻找不到则触发GamereError
    title='gamere window', # 窗口标题
    size=(1000, 1000),  # 窗口大小
    flags=0, # 窗口模式，请参照pygame窗口模式
    depth=0,  # 请参照pygame窗口depth
    display=0,  # 请参照pygame窗口display
    fps=20,    # FPS 
    icon=None,  # 窗口图标
    running=True,  # 是否运行
    music=None,  # 背景音乐
    bgm=None,   # 同music参数
    texts=None, # font模式下的text矩阵
)
```

####str
返回“gamere.cpp.Window”

####sleep
闪烁
```python
window.sleep(secs=0.1)
```
在0.0.1版本中，secs参数无意义

####quit
关闭窗口和程序
```python
window.quit(*args, **kwargs)
```

####destroy
关闭窗口和程序
```python
window.destroy(code, /)
```

####spat
关闭窗口，进入last
```python
window.spat()
```

####get
返回窗口的pygame.Surface对象
```python
surface = window.get()
```

####loop
主循环
```python
window.loop(
    handler=_pass,  # 事件判断函数
    render=_pass,   # 绘图函数
    update=_pass,   # 更新函数
    last=_pass,    # 窗口spat后的执行
    start=gamere.init,    # 初始化函数
    mode=False,    # 事件判断函数的输入是否设为pygame.key.get_mods()
    press=False,   # 事件判断函数的输入是否设为pygame.key.get_pressed()
    font=None,    # font模式下的字体路径
    size=16,     # font模式下的大小
    fwidth=16,   # font模式下的长
    fheight=16,  # font模式下的宽
    loops=0)
```
