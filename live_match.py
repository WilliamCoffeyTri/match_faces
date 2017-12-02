import os
import sys
import cv2
import shutil
import json
from match import compare_known_to_unknowns, test_image_output_json

def print_output(output):
	for json_obj in json.loads(output):
		for item in json_obj:
			for key in item:
				print item[key]

def camera(known):
	cam = cv2.VideoCapture(0)

	cv2.namedWindow("test")

	img_counter = 0

	while True:
	    ret, frame = cam.read()
	    cv2.imshow("test", frame)
	    if not ret:
	        break
	    k = cv2.waitKey(1)

	    if k%256 == 27:
	        # ESC pressed
	        print("Escape hit, closing...")
	        break
	    elif k%256 == 32:
	        # SPACE pressed
    		os.makedirs(str(img_counter))
	        img_name = os.path.join(str(img_counter), "opencv_frame_{}.png".format(img_counter))
	        cv2.imwrite(img_name, frame)
	        print("Image {} captured!".format(img_name))
	        output = compare_known_to_unknowns(known, str(img_counter))
	        print_output(output)
	        shutil.rmtree(str(img_counter), ignore_errors=False, onerror=None)
	        img_counter += 1

	        

	cam.release()

	cv2.destroyAllWindows()

def usage():
	print "Usage: python live_match.py [known folder]"

def main():
	if len(sys.argv) == 2:
		known = sys.argv[1]
		if known:
			camera(known)
		else:
			print "invalid input"
			exit(0)

	else:
		usage()

if __name__ == "__main__":
	main()