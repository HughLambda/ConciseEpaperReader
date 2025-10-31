
import machine
import time
import sys

class EPDDiagnostic:
    def __init__(self):
        # Pin definitions
        self.RST_PIN = machine.Pin(5, machine.Pin.OUT)
        self.DC_PIN = machine.Pin(6, machine.Pin.OUT)
        self.CS_PIN = machine.Pin(7, machine.Pin.OUT)
        self.BUSY_PIN = machine.Pin(8, machine.Pin.IN)
        
        # Initialize pin states
        self.RST_PIN.value(1)
        self.DC_PIN.value(0)
        self.CS_PIN.value(1)
        
        # SPI initialization
        try:
            self.spi = machine.SPI(0,
                                baudrate=4000000,
                                polarity=0,
                                phase=0,
                                bits=8,
                                firstbit=machine.SPI.MSB,
                                sck=machine.Pin(2),
                                mosi=machine.Pin(3))
            print("✓ SPI initialization successful")
        except Exception as e:
            print(f"✗ SPI initialization failed: {e}")
            return
        
        self.WIDTH = 296
        self.HEIGHT = 128
        
    def test_pins(self):
        """Test all GPIO pins"""
        print("\n=== Pin Testing ===")
        pins = [
            (self.RST_PIN, "RST"),
            (self.DC_PIN, "DC"), 
            (self.CS_PIN, "CS"),
            (self.BUSY_PIN, "BUSY")
        ]
        
        for pin, name in pins:
            try:
                if name == "BUSY":
                    value = pin.value()
                    print(f"✓ {name} pin: {value}")
                else:
                    print(f"✓ {name} pin: Normal")
            except Exception as e:
                print(f"✗ {name} pin abnormal: {e}")
    
    def test_spi(self):
        """Test SPI communication"""
        print("\n=== SPI Communication Test ===")
        try:
            # Send test data
            test_data = bytearray([0xAA, 0x55, 0x01, 0x02])
            self.spi.write(test_data)
            print("✓ SPI data transmission normal")
            return True
        except Exception as e:
            print(f"✗ SPI communication failed: {e}")
            return False
    
    def test_power(self):
        """Test power status"""
        print("\n=== Power Supply Test ===")
        try:
            # Read 3.3V pin voltage (approximate)
            adc = machine.ADC(machine.Pin(29))  # VSYS pin
            voltage = adc.read_u16() * 3.3 / 65535
            print(f"✓ System voltage: {voltage:.2f}V")
            return voltage > 3.0
        except:
            print("⚠ Unable to detect voltage, please check manually")
            return True
    
    def hard_reset(self):
        """Hardware reset the screen"""
        print("Performing hardware reset...")
        self.RST_PIN.value(0)
        time.sleep_ms(100)
        self.RST_PIN.value(1)
        time.sleep_ms(100)
        print("✓ Hardware reset completed")
    
    def check_busy_state(self):
        """Check BUSY pin status"""
        print("\n=== BUSY Status Check ===")
        busy_value = self.BUSY_PIN.value()
        print(f"BUSY pin status: {busy_value}")
        if busy_value == 0:
            print("⚠ Screen may be in busy state")
        else:
            print("✓ Screen is idle")
        return busy_value
    
    def send_init_sequence(self):
        """Send initialization sequence"""
        print("\n=== Initialization Sequence ===")
        
        # Common e-paper initialization commands
        init_commands = [
            (0x12, "SWRESET - Software Reset"),
            (0x01, "DRIVER_OUTPUT_CONTROL - Driver Output Control"),
            (0x11, "DATA_ENTRY_MODE - Data Entry Mode"),
            (0x44, "SET_RAM_X_ADDRESS - Set RAM X Address"),
            (0x45, "SET_RAM_Y_ADDRESS - Set RAM Y Address"),
            (0x3C, "BORDER_WAVEFORM_CONTROL - Border Waveform Control"),
            (0x21, "DISPLAY_UPDATE_CONTROL - Display Update Control"),
            (0x4E, "SET_RAM_X_ADDRESS_COUNTER - Set RAM X Address Counter"),
            (0x4F, "SET_RAM_Y_ADDRESS_COUNTER - Set RAM Y Address Counter"),
            (0x24, "WRITE_RAM - Write RAM")
        ]
        
        for cmd, desc in init_commands:
            try:
                self.send_command(cmd)
                print(f"✓ {desc}: 0x{cmd:02X}")
                time.sleep_ms(10)
            except Exception as e:
                print(f"✗ {desc} failed: {e}")
    
    def send_command(self, command):
        """Send command"""
        self.DC_PIN.value(0)
        self.CS_PIN.value(0)
        self.spi.write(bytearray([command]))
        self.CS_PIN.value(1)
    
    def send_data(self, data):
        """Send data"""
        self.DC_PIN.value(1)
        self.CS_PIN.value(0)
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.CS_PIN.value(1)
    
    def test_display_pattern(self):
        """Test display patterns"""
        print("\n=== Display Testing ===")
        
        # Test 1: All white
        print("Test 1: All white display...")
        self.send_command(0x24)
        for i in range(min(100, self.WIDTH * self.HEIGHT // 8)):
            self.send_data(0xFF)
        
        self.send_command(0x20)  # Activate display
        time.sleep(20)
        
        # Test 2: All black
        print("Test 2: All black display...")
        self.send_command(0x24)
        for i in range(min(100, self.WIDTH * self.HEIGHT // 8)):
            self.send_data(0x00)
        
        self.send_command(0x20)  # Activate display
        time.sleep_ms(2000)
        
        # Test 3: Checkerboard pattern
        print("Test 3: Checkerboard pattern...")
        self.send_command(0x24)
        for i in range(min(100, self.WIDTH * self.HEIGHT // 8)):
            self.send_data(0xAA if i % 2 == 0 else 0x55)
        
        self.send_command(0x20)  # Activate display
        print("✓ Display testing completed")
    
    def run_full_diagnostic(self):
        """Run complete diagnostic"""
        print("Starting E-paper Diagnostic...")
        print("=" * 50)
        
        # 1. Pin testing
        self.test_pins()
        
        # 2. Power testing  
        if not self.test_power():
            print("⚠ Power voltage might be insufficient")
        
        # 3. SPI testing
        if not self.test_spi():
            print("✗ SPI communication abnormal, please check connections")
            return False
        
        # 4. Hardware reset
        self.hard_reset()
        
        # 5. Check BUSY status
        self.check_busy_state()
        
        # 6. Initialization sequence
        self.send_init_sequence()
        
        # 7. Display testing
        self.test_display_pattern()
        
        print("\n" + "=" * 50)
        print("Diagnostic completed!")
        return True

def main():
    print("Pico W E-paper Diagnostic Tool")
    print("Screen Model: 296x128 Black/White/Red")
    print("Connection Check:")
    print("SCK -> GP2, SDA -> GP3")
    print("RST -> GP5, DC -> GP6, CS -> GP7, BUSY -> GP8")
    
    diagnostic = EPDDiagnostic()
    success = diagnostic.run_full_diagnostic()
    
    if success:
        print("\n✅ Diagnostic successful! If screen still no response:")
        print("1. Check screen model and initialization commands")
        print("2. Confirm SPI mode and frequency")
        print("3. Verify power supply stability")
    else:
        print("\n❌ Diagnostic found abnormalities, please check according to above prompts")

if __name__ == "__main__":
    main()