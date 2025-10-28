
# import machine
# import time

# class EPDDriver:
#     def __init__(self):
#         # 引脚定义
#         self.RST_PIN = machine.Pin(5, machine.Pin.OUT)
#         self.DC_PIN = machine.Pin(6, machine.Pin.OUT)
#         self.CS_PIN = machine.Pin(7, machine.Pin.OUT)
#         self.BUSY_PIN = machine.Pin(8, machine.Pin.IN)
        
#         # SPI初始化
#         self.spi = machine.SPI(0,
#                             baudrate=4000000,
#                             polarity=0,
#                             phase=0,
#                             bits=8,
#                             firstbit=machine.SPI.MSB,
#                             sck=machine.Pin(2),
#                             mosi=machine.Pin(3))
        
#         # 屏幕参数
#         self.WIDTH = 296
#         self.HEIGHT = 128
        
#     def reset(self):
#         """复位屏幕"""
#         self.RST_PIN.value(1)
#         time.sleep_ms(10)
#         self.RST_PIN.value(0)
#         time.sleep_ms(10)
#         self.RST_PIN.value(1)
#         time.sleep_ms(10)
        
#     def send_command(self, command):
#         """发送命令"""
#         self.DC_PIN.value(0)
#         self.CS_PIN.value(0)
#         self.spi.write(bytearray([command]))
#         self.CS_PIN.value(1)
        
#     def send_data(self, data):
#         """发送数据"""
#         self.DC_PIN.value(1)
#         self.CS_PIN.value(0)
#         if isinstance(data, int):
#             self.spi.write(bytearray([data]))
#         else:
#             self.spi.write(data)
#         self.CS_PIN.value(1)
        
#     def wait_until_idle(self):
#         """等待屏幕空闲"""
#         while self.BUSY_PIN.value() == 0:
#             time.sleep_ms(10)
            
#     def init_display(self):
#         """初始化显示"""
#         self.reset()
        
#         # 发送初始化命令序列
#         self.send_command(0x12)  # 软件复位
#         self.wait_until_idle()
        
#         # 这里需要根据你的具体屏幕型号添加正确的初始化命令
#         print("Display initialized")
        
#     def clear_screen(self):
#         """清屏"""
#         self.send_command(0x10)
#         for i in range(self.WIDTH * self.HEIGHT // 8):
#             self.send_data(0xFF)
            
#         self.send_command(0x13)
#         for i in range(self.WIDTH * self.HEIGHT // 8):
#             self.send_data(0x00)
            
#         self.send_command(0x12)  # 刷新显示
#         self.wait_until_idle()
        
#     def display_text(self, text, x=0, y=0):
#         """显示文本（基础功能）"""
#         # 这里需要实现字符渲染逻辑
#         print(f"Display text: {text} at ({x}, {y})")

# # 主程序
# def main():
#     epd = EPDDriver()
#     epd.init_display()
#     epd.clear_screen()
#     epd.display_text("Hello E-Paper!")
    
# if __name__ == "__main__":
#     main()


import machine
import time
import sys

class EPDDriver:
    def __init__(self):
        # 引脚定义
        self.RST_PIN = machine.Pin(5, machine.Pin.OUT)
        self.DC_PIN = machine.Pin(6, machine.Pin.OUT)
        self.CS_PIN = machine.Pin(7, machine.Pin.OUT)
        self.BUSY_PIN = machine.Pin(8, machine.Pin.IN)
        
        # 初始化引脚状态
        self.RST_PIN.value(1)
        self.CS_PIN.value(1)
        
        # SPI初始化
        try:
            self.spi = machine.SPI(0,
                                baudrate=4000000,
                                polarity=0,
                                phase=0,
                                bits=8,
                                firstbit=machine.SPI.MSB,
                                sck=machine.Pin(2),
                                mosi=machine.Pin(3))
            print("1SPI初始化成功")
        except Exception as e:
            print(f"2SPI初始化失败: {e}")
            raise
        
        # 屏幕参数
        self.WIDTH = 296
        self.HEIGHT = 128
        
    def reset(self):
        """复位屏幕"""
        print("3正在复位屏幕...")
        self.RST_PIN.value(1)
        time.sleep_ms(10)
        self.RST_PIN.value(0)
        time.sleep_ms(10)
        self.RST_PIN.value(1)
        time.sleep_ms(10)
        print("4屏幕复位完成")
        
    def send_command(self, command):
        """发送命令"""
        self.DC_PIN.value(0)
        self.CS_PIN.value(0)
        self.spi.write(bytearray([command]))
        self.CS_PIN.value(1)
        print(f"5发送命令: 0x{command:02X}")
        
    def send_data(self, data):
        """发送数据"""
        self.DC_PIN.value(1)
        self.CS_PIN.value(0)
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.CS_PIN.value(1)
        
    def wait_until_idle(self, timeout=5000):
        """等待屏幕空闲，增加超时机制"""
        print("6等待屏幕空闲...")
        start_time = time.ticks_ms()
        
        while self.BUSY_PIN.value() == 0:
            if time.ticks_diff(time.ticks_ms(), start_time) > timeout:
                print("7等待屏幕超时！")
                return False
            time.sleep_ms(10)
            
        print("8屏幕准备就绪")
        return True
        
    def init_display(self):
        """初始化显示"""
        print("9开始初始化显示...")
        self.reset()
        
        try:
            # 发送初始化命令序列
            self.send_command(0x12)  # 软件复位
            time.sleep_ms(10)
            
            if not self.wait_until_idle():
                print("10初始化失败：屏幕无响应")
                return False
                
            # 这里需要根据你的具体屏幕型号添加正确的初始化命令
            # 示例命令序列（可能需要调整）
            commands = [
                (0x01, [0x27, 0x01, 0x00]),  # 驱动输出控制
                (0x11, [0x03]),  # 数据输入模式
                (0x44, [0x00, 0x0F]),  # 设置RAM X地址
                (0x45, [0x00, 0x00, 0x27, 0x01]),  # 设置RAM Y地址
                (0x3C, [0x05]),  # 边界波形控制
                (0x21, [0x00, 0x80]),  # 显示更新控制
            ]
            
            for cmd, data in commands:
                self.send_command(cmd)
                if data:
                    for d in data:
                        self.send_data(d)
                time.sleep_ms(5)
                
            print("11显示初始化完成")
            return True
            
        except Exception as e:
            print(f"12初始化过程中出错: {e}")
            return False
        
    def clear_screen(self):
        """清屏"""
        print("13正在清屏...")
        self.send_command(0x10)
        for i in range(self.WIDTH * self.HEIGHT // 8):
            self.send_data(0xFF)
            
        self.send_command(0x13)
        for i in range(self.WIDTH * self.HEIGHT // 8):
            self.send_data(0x00)
            
        self.send_command(0x12)  # 刷新显示
        if self.wait_until_idle():
            print("1清屏完成i")
        else:
            print("2清屏过程中屏幕无响应j")

# 主程序
def main():
    try:
        epd = EPDDriver()
        if epd.init_display():
            epd.clear_screen()
            print("3电子阅读器驱动测试成功！a")
        else:
            print("4初始化失败，请检查硬件连接b")
            
    except KeyboardInterrupt:
        print("5程序被用户中断c")
    except Exception as e:
        print(f"6程序运行出错: d{e}")
        print("7建议检查：e")
        print("1. 硬件连接是否正确f")
        print("2. 屏幕型号是否匹配g")
        print("3. 电源是否稳定h")
    
if __name__ == "__main__":
    main()
