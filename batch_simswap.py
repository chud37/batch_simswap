import pathlib
import sys
import os
from os import path
import subprocess
from datetime import date


## ------------------------------
## Paths / Directories.  Change as needed.
## ------------------------------
faces_input_path = './input_faces'
video_input_path = 'p:/imgs/simswap/input'
video_output_path = 'p:/imgs/simswap'



## ------------------------------
## Input Face
## ------------------------------
try:
    face = sys.argv[1]
except IndexError:
    face = ''

## ------------------------------
## Set Arg[2] to show only generated commands (useful for creating a batch file to run overnight)
## ------------------------------
try:
    generate_commands_only = sys.argv[2]
except IndexError:
    generate_commands_only = 0






selectedface = ''
simswap_command = "python test_video_swapsingle.py --isTrain false --use_mask --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path ./__input_selected_face__ --video_path __input_video_file__ --output_path __output_file_name__ --temp_path ./temp_results --no_simswaplogo"
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
        print("\t", "Unable to create ouput directory:",faces_input_path)
    exit = 1

if not path.exists(video_input_path):
    print('WARNING: Cannot find ',video_input_path, 'directory.  Attempting to create..')
    try:
        os.mkdir(video_input_path)
        print("\t", video_input_path, "has been created. Please put some MP4 files in there to start.")
    except:
        print("\t", "Unable to create input path directory:",video_input_path)
    exit = 1

if exit: sys.exit()




## ------------------------------
## Find file for faces
## ------------------------------
for file in pathlib.Path(faces_input_path).iterdir():
    if file.is_file():
        if face in str(file):
            selectedface = str(file)
            break

## ------------------------------
## Find input video(s)
## ------------------------------
inputvideos = []
for file in pathlib.Path(video_input_path).iterdir():
    if file.is_file():
        if '.mp4' in str(file):
            inputvideos.append(file)
        if '.webm' in str(file):
            newfilename = str(file).replace(".webm",".mp4")
            os.rename(file, newfilename)
            inputvideos.append(newfilename)

## ------------------------------
## Generate & Run Each Command for every video
## ------------------------------
if selectedface and (len(inputvideos) > 0):
    print('Selected Face:')
    print('\t',selectedface)
    print('Input Videos: ')
    for videofile in inputvideos:
        print('\t', videofile)

    counter = 0

    today = date.today()

    for videofile in inputvideos:
        output_video_file_path = video_output_path + "/" + face + "/" + today.strftime("%m-%d-%y") + "/"
        output_video_filename = os.path.basename(videofile)
        compiled_command = simswap_command.replace('__input_selected_face__', selectedface.replace('\\','/'))
        compiled_command = compiled_command.replace('__input_video_file__', '"' + str(videofile).replace('\\','/') + '"')
        compiled_command = compiled_command.replace('__output_file_name__', output_video_file_path + '"' + output_video_filename + '"')
        
        counter += 1
        
        # Check if the folder exists, if not, create it.
        if not path.exists(output_video_file_path):
            try:
                os.makedirs(output_video_file_path)
                print(" [Successfully created directory:", output_video_file_path,"]")
            except OSError as exc:
                print(" [Unable to create directory: " + output_video_file_path + " Error: "+exc+"]")
                sys.exit()

        
        if generate_commands_only:
            print(compiled_command)
        else:

            print('\n----------------------------------')
            print(" PROCESSING: " + os.path.basename(videofile) + " with face: " + face +" (Video " + str(counter) + " of " + str(len(inputvideos)) + ")")
            print(' Output filename: ' + output_video_file_path + output_video_filename)
            print('----------------------------------')

            subprocess.run(compiled_command, stdout=subprocess.DEVNULL)
            os.remove(videofile)
            # Use the below to show the output and diagnose any errors you might be getting. (Comment out the above first)
            # subprocess.run(compiled_command)

    print('\n\nSIMSWAP BATCH: FINISHED.\n\n')
    # subprocess.Popen(r'explorer /select "'+output_video_file_path+'"')
    if not generate_commands_only: 
        os.startfile(os.path.realpath(output_video_file_path))

elif not selectedface:
    print('WARNING: No selected face found.  Did you pass a parameter?  Correct syntax is python batch_swimswap.py john')
elif(len(inputvideos) == 0):
    print('WARNING: No input videos found in',video_input_path)