from pynput import keyboard


class MyDataStructure:
    def __init__(self):
        self.ball = []
        self.skill = ['', '']

    def add_ball(self, item):
        self.ball.append(item)
        if len(self.ball) > 3:
            self.ball = self.ball[-3:]

    def add_skill(self, item):
        if (item != self.skill[0] and item != self.skill[1]):
            self.skill[1] = self.skill[0]
            self.skill[0] = item

    def gen_skill(self):
        if len(self.ball) == 3:
            str = self.ball[0] + self.ball[1] + self.ball[2]
            print("skill" + str)
            self.add_skill(str)

    def release_skill(self, i):
        print("release" + self.skill[i - 1])
        # read_and_print_file("11.txt")


my_data = MyDataStructure()


def on_press(key):
    # 判断key是否为 q w e
    try:
        if key.char in ['q', 'w', 'e']:
            my_data.add_ball(key.char)
            print(my_data.ball)
        if key.char in ['r']:
            my_data.gen_skill()
        if key.char == 'd':
            my_data.release_skill(1)
        if key.char == 'f':
            my_data.release_skill(2)
    except AttributeError:
        pass


def on_release(key):
    if key == keyboard.Key.esc:
        # 停止监听器
        return False
def read_and_print_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    # 创建一个监听器
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    # 启动监听器
    listener.start()
    # 保持主线程运行
    while True:
        pass
