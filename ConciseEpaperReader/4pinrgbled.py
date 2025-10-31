
import machine
import time
import random

# 配置RGB LED引脚（根据您的实际接线调整）
RED_PIN = 0
GREEN_PIN = 1
BLUE_PIN = 2

# 初始化PWM引脚
red_pwm = machine.PWM(machine.Pin(RED_PIN))
green_pwm = machine.PWM(machine.Pin(GREEN_PIN))
blue_pwm = machine.PWM(machine.Pin(BLUE_PIN))

# 设置PWM频率
red_pwm.freq(1000)
green_pwm.freq(1000)
blue_pwm.freq(1000)

def set_color(red, green, blue):
    """
    设置RGB颜色
    参数范围: 0-255
    """
    # 将0-255转换为0-65535的PWM占空比
    red_pwm.duty_u16(int(red * 257))  # 255 * 257 = 65535
    green_pwm.duty_u16(int(green * 257))
    blue_pwm.duty_u16(int(blue * 257))

def color_cycle():
    """颜色循环效果"""
    colors = [
        (255, 0, 0),    # 红色
        (0, 255, 0),    # 绿色
        (0, 0, 255),    # 蓝色
        (255, 255, 0),  # 黄色
        (255, 0, 255),  # 紫色
        (0, 255, 255),  # 青色
        (255, 255, 255) # 白色
    ]
    
    for color in colors:
        set_color(*color)
        print(f"颜色: RGB{color}")
        time.sleep(1)

def fade_effect():
    """渐变效果"""
    steps = 50
    for i in range(steps):
        # 红色渐变到绿色
        red = int(255 * (1 - i/steps))
        green = int(255 * (i/steps))
        set_color(red, green, 0)
        time.sleep(0.05)
    
    for i in range(steps):
        # 绿色渐变到蓝色
        green = int(255 * (1 - i/steps))
        blue = int(255 * (i/steps))
        set_color(0, green, blue)
        time.sleep(0.05)
    
    for i in range(steps):
        # 蓝色渐变到红色
        blue = int(255 * (1 - i/steps))
        red = int(255 * (i/steps))
        set_color(red, 0, blue)
        time.sleep(0.05)

def random_color():
    """随机颜色"""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    set_color(red, green, blue)
    print(f"随机颜色: RGB({red}, {green}, {blue})")

def breathing_effect(color=(255, 0, 0), duration=3):
    """呼吸灯效果"""
    steps = 100
    for i in range(steps):
        brightness = (i / steps) ** 2  # 使用平方曲线使效果更自然
        red = int(color[0] * brightness)
        green = int(color[1] * brightness)
        blue = int(color[2] * brightness)
        set_color(red, green, blue)
        time.sleep(duration / steps / 2)
    
    for i in range(steps, 0, -1):
        brightness = (i / steps) ** 2
        red = int(color[0] * brightness)
        green = int(color[1] * brightness)
        blue = int(color[2] * brightness)
        set_color(red, green, blue)
        time.sleep(duration / steps / 2)

def main():
    print("RGB LED控制器启动")
    print("=" * 30)
    
    try:
        while True:
            print("\n选择模式:")
            print("1 - 颜色循环")
            print("2 - 渐变效果")
            print("3 - 随机颜色")
            print("4 - 红色呼吸灯")
            print("5 - 绿色呼吸灯")
            print("6 - 蓝色呼吸灯")
            print("q - 退出")
            
            choice = input("请输入选择: ").strip().lower()
            
            if choice == '1':
                print("开始颜色循环...")
                color_cycle()
            elif choice == '2':
                print("开始渐变效果...")
                fade_effect()
            elif choice == '3':
                print("生成随机颜色...")
                random_color()
            elif choice == '4':
                print("红色呼吸灯...")
                breathing_effect((255, 0, 0))
            elif choice == '5':
                print("绿色呼吸灯...")
                breathing_effect((0, 255, 0))
            elif choice == '6':
                print("蓝色呼吸灯...")
                breathing_effect((0, 0, 255))
            elif choice == 'q':
                print("退出程序")
                break
            else:
                print("无效选择，请重试")
                
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        # 关闭所有LED
        set_color(0, 0, 0)
        red_pwm.deinit()
        green_pwm.deinit()
        blue_pwm.deinit()
        print("LED已关闭，程序结束")

if __name__ == "__main__":
    main()