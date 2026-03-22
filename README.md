# IoT Firmware Extractor
This is a python based firmware extraction script that automates the flash_dump process over UART to extract the full firmware. This emulates a human-like interface over the UART shell using pexpect, as many embedded applications, specially some RTOS systems prevents automating UART commands.  

Getting Started
1. Clone the Repository : 
git clone https://github.com/parichoy-ghosal/iot-firmware-extractor.git
cd iot-firmware-extractor

2. Install Dependencies
Make sure you have Python installed. Then install required tools:
pip install -r requirements.txt 

3. Modify Parameters
Before running the flash_dump.py script, make sure to edit it to adjust the baudrate(BAUD) and COM port(PORT), as well as the end address(END_ADDR) and step count(STEP) according to the embedded device and UART connection.

4. Run the Script
python3 flash_dump.py

The output is saved in the same directory with the script, named as 'firmware.bin'.

[Note : Please make sure the UART connection from the embedded device is connected to the PC before running the script.]

Feel free to leave feedback! Stay Electric!
