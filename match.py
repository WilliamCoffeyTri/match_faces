import json
import os
import sys
import face_recognition_api.face_recognition.api as face_recognition
from face_recognition_api.face_recognition.cli import test_image, scan_known_people, image_files_in_folder


def compare_known_to_unknowns(known, unknown):
    known_images_folder = os.path.join(os.getcwd(), known)
    unknown_images_folder = os.path.join(os.getcwd(), unknown)
    known_names, known_face_encodings = scan_known_people(known_images_folder)
    output = [test_image_output_json(image_file, known_names, known_face_encodings) for image_file in image_files_in_folder(unknown_images_folder)]

    return json.dumps(output)

def test_image_output_json(image_to_check, known_names, known_face_encodings):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if unknown_image.shape[1] > 1600:
        scale_factor = 1600.0 / unknown_image.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            unknown_image = scipy.misc.imresize(unknown_image, scale_factor)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    output = list()

    for unknown_encoding in unknown_encodings:
        result = face_recognition.compare_faces(known_face_encodings, unknown_encoding)

        if True in result:
            [output.append({'imagePath': image_to_check, 'name': name}) for is_match, name in zip(result, known_names) if is_match]
        else:
            [output.append({'imagePath': image_to_check, 'name': 'unknown_name'})]

    return output

def usage():
	print "Usage: python match.py [known folder] [unknown folder]"

def main():
	if len(sys.argv) == 3:
		known, unknown = sys.argv[1:]
		if known and unknown:
			output = compare_known_to_unknowns(known, unknown)
			print output

	else:
		usage()

if __name__ == "__main__":
	main()
