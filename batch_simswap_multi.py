import pathlib
import sys
import os
from os import path
import subprocess
from shutil import copyfile

## ------------------------------
## Input Faces
## ------------------------------
# Face 1
try:
    face_a = sys.argv[1]
except IndexError:
    face_a = ''

# Face 2
try:
    face_b = sys.argv[2]
except IndexError:
    face_b = ''

## ------------------------------
## Set Arg[3] to show only generated commands (useful for creating a batch file to run overnight)
## ------------------------------
try:
    generate_commands_only = sys.argv[3]
except IndexError:
    generate_commands_only = 0


selectedface_a = ''
selectedface_b = ''
faces_input_path = './input_faces'
video_input_path = 'p:/imgs/simswap/input'
video_output_path = 'p:/imgs/simswap'
multispecific_path = './multispecific'
simswap_command = "python test_video_swap_multispecific.py --isTrain false --use_mask --name people --Arc_path arcface_model/arcface_checkpoint.tar --video_path __input_video_file__ --output_path __output_file_name__ --temp_path ./temp_results --multisepcific_dir __multi_specific_path__ --no_simswaplogo"
exit = 0

print('\n')

## ------------------------------
## PATH CHECKS
## ------------------------------
if not path.exists(faces_input_path): 
    print('WARNING: Cannot find ',faces_input_path, 'directory.  Attempting to create..')
    try:
        os.mkdir(faces_input_path)
        print("\t", faces_input_path, "has been created. Please put some JPG/PNG files in there to start.")
    except:
        print("\t", "Unable to create directory:",faces_input_path)
    exit = 1

if not path.exists(video_input_path):
    print('WARNING: Cannot find ',video_input_path, 'directory.  Attempting to create..')
    try:
        os.mkdir(video_input_path)
        print("\t", video_input_path, "has been created. Please put some MP4 files in there to start.")
    except:
        print("\t", "Unable to create directory:",video_input_path)
    exit = 1

if exit: sys.exit()

## ------------------------------
## Find files for faces
## ------------------------------
for file in pathlib.Path(faces_input_path).iterdir():
    if file.is_file():
        if face_a in str(file):
            selectedface_a = str(file)

for file in pathlib.Path(faces_input_path).iterdir():
    if file.is_file():
        if face_b in str(file):
            selectedface_b = str(file)

## ------------------------------
## Find input video(s)
## ------------------------------
inputvideos = []
for file in pathlib.Path(video_input_path).iterdir():
    if file.is_file():
        if '.mp4' in str(file):
            inputvideos.append(file)

## ------------------------------
## Generate & Run Each Command for every video
## ------------------------------
if selectedface_a and selectedface_b and (len(inputvideos) > 0):
    
    print('Selected faces:')
    print('\t',selectedface_a, selectedface_b)

    # Copy faces to multispecific folder
    copyfile(selectedface_a, multispecific_path + "/DST_01.png")
    copyfile(selectedface_b, multispecific_path + "/DST_02.png")

    print('Input Videos: ')
    for videofile in inputvideos:
        print('\t', videofile)


    counter = 0

    for videofile in inputvideos:
        output_video_file_path = video_output_path + "/" + face_a + "-" + face_b + "/"
        output_video_filename = os.path.basename(videofile)
        compiled_command = simswap_command.replace('__input_video_file__', '"' + str(videofile).replace('\\','/') + '"')
        compiled_command = compiled_command.replace('__multi_specific_path__', multispecific_path.replace('\\','/'))
        compiled_command = compiled_command.replace('__output_file_name__', output_video_file_path + '"' + output_video_filename + '"')
        
        counter += 1

        print('\n----------------------------------')
        print(" PROCESSING: " + os.path.basename(videofile) + " with face: " + face_a + " and " + face_b + " (Video " + str(counter) + " of " + str(len(inputvideos)) + ")")
        print(' Output filename: ' + output_video_file_path + output_video_filename)

        # Check if the folder exists, if not, create it.
        if not path.exists(output_video_file_path):
            try:
                os.mkdir(output_video_file_path)
                print(" [Successfully created directory:", output_video_file_path,"]")
            except:
                print(" [Unable to create directory:",video_input_path,", program fail.]")
                sys.exit()

        print('----------------------------------')
        if generate_commands_only:
            print(compiled_command)
        else:
            subprocess.run(compiled_command, stdout=subprocess.DEVNULL)
            # Use the below to show the output and diagnose any errors you might be getting. (Comment out the above first)
            # subprocess.run(compiled_command)
        
    print('\n\nSIMSWAP BATCH: FINISHED.\n\n')
elif not selectedface_a:
    print('WARNING: No selected face A found.  Did you pass a parameter?  Correct syntax is python batch_swimswap.py john')
elif not selectedface_b:
    print('WARNING: No selected face B found.  Did you pass a parameter?  Correct syntax is python batch_swimswap.py john')    
elif(len(inputvideos) == 0):
    print('WARNING: No input videos found in',video_input_path)