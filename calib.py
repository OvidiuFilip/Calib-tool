import re
import sys
import os

help = """
=========================================================================================
| Calib tool										|
=========================================================================================
|											|
| Calib tool generates a calibration matrix for current touchscreen controller.		|
|											|
| Generate calib_file using 'DISPLAY=:0.0 xinput_calibrator -v > calib_file' command.	|
|											|
| Params order: python3 calib.py path_to_calib_file screen_width screen_height		|
|											|
=========================================================================================
"""

def main():
	nr_args = len(sys.argv)
	if nr_args < 4:
		cls()
		print(help)
	elif nr_args == 4:
		try:
			calib_file=str(sys.argv[1])
			screen_width=int(sys.argv[2])
			screen_height=int(sys.argv[3])
			calculate(calib_file, screen_width, screen_height)
		except:
			cls()
			print(help)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
	
def parse_model(line):
	match = re.search("\'(.+?)\'", line).group(1)
	return str(match)
	
def parse_coords(line):
	match = re.search('\((.+?)\)', line).group(1)
	pieces = match.split(',')
	x = int(pieces[0].split('=')[1])
	y = int(pieces[1].split('=')[1])
	return x,y

def get_touch_data(file):
	temp_list = []
	model = None
	try:
		fp = open(file, 'r')
		for line in fp:
			if "DEBUG: Adding click 0" in line:
				x,y = parse_coords(line)
				temp_list.append(x)
				temp_list.append(y)
				
			if "DEBUG: Adding click 3" in line:
				x,y = parse_coords(line)
				temp_list.append(x)
				temp_list.append(y)
				
			if "DEBUG: Found" in line and model == None:
				model=parse_model(line)
				
	finally:
		fp.close()
	return temp_list,model


def calculate(calib_file, screen_width, screen_height):
	
	coord_list,model = get_touch_data(calib_file)
	click_0_X=coord_list[0]
	click_0_Y=coord_list[1]

	click_3_X=coord_list[2]
	click_3_Y=coord_list[3]

	a = (screen_width * 6 / 8) / (click_3_X - click_0_X)
	c = ((screen_width / 8) - (a * click_0_X)) / screen_width
	e = (screen_height * 6 / 8) / (click_3_Y - click_0_Y)
	f = ((screen_height / 8) - (e * click_0_Y)) / screen_height
	print("Screen size: "+str(screen_width)+" x "+str(screen_height))
	print("Touchscreen calibration matrix command: ")
	print(" DISPLAY=:0.0 xinput set-prop \""+model+"\" --type=float \"libinput Calibration Matrix\" "+str(a)+", 0.0, "+str(c)+", 0.0, "+str(e)+", "+str(f)+", 0.0, 0.0, 1.0")
	
if __name__ == "__main__":
	main()
