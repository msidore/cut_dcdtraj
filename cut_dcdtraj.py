#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, subprocess, os
from argparse import ArgumentParser

""" Usage: ./cut_dcdtraj -f trajectory.dcd -p topology.psf -wf number_slice -cd catdcd_location [-nf numframes, -d directory] """

######################## Parsing stuff ########################

# Defaults
directory = ""
trajectory = ""
psf = ""
wFrames = ""
numFrames = ""
catdcd_loc = ""
gromacs = False

parser = ArgumentParser(description=""" Using catdcd, cuts a .dcd trajectory into slices with the specified number of frames\n
MDAnalysis is only used to get the number of frames if it is not specified.  """)

# Named arguments
parser.add_argument("-f", "--file", help="The name of the input .dcd file.")
parser.add_argument("-p", "--psf", help="The name of the .psf (topology) file.")
parser.add_argument("-wf", "--wframes", help="The number of frames per slice. - 20000 ~= 7Go")
parser.add_argument("-nf", "--numframes", help="The total number of frames in the trajectory, if known.")
parser.add_argument("-cd", "--catdcd", help="The location of the catdcd executable.")
parser.add_argument("-o", "--output", help="The generic name of the output.")

# Optional arguments
parser.add_argument("-d", "--directory", help="Output directory ? Default is the current directory.")
parser.add_argument("-trr", "--gromacs", help="Is it a gromacs trr trajectory ? Uses trjconv to split everything !")

args = parser.parse_args()

######################## Directory stuff ########################

if args.directory:
    # Checks if the directory has a /
    if args.directory[-1] == "/":
        directory += args.directory
    else:
        directory += args.directory + "/"
    os.system("mkdir " + directory)

######################## Samples ########################

# Number of frames per trajectory
wFrames = 10000

# Trajectory and topology
#~ directory = "/media/ubuntu/DATA/Trajectories/ABFdist/ABFd/"
#~ pathName = "/media/ubuntu/DATA/Trajectories/ABFdist/ABFn/"
#trajName = "80100-70_protlipids.wrapp.dcd"
#~ trajName = "MonoA.wrapp.dcd"
trajectory = "/media/ubuntu/DATA/Trajectories/ABFdist/ABFd/ABFd0-23.dcd"
outName = "ABFd"
psf = "/media/ubuntu/DATA/Miscellaneous/DimerAqpZ.psf"
#~ psf = "/media/ubuntu/DATA/Miscellaneous/init_AqpZ_protlipids.psf"
#~ psf = "/media/ubuntu/DATA/Miscellaneous/monomer-AqpZ.psf"

# Location of catdcd
catdcd_loc = "/home/ubuntu/bin/catdcd"
#catdcd_loc = "/home/marlon/bin/catdcd"

######################## Parser checking stuff ########################
# /!\ Everything is optional here because of the samples provided up there, because I find it handy to simply write the many arguments in the script

# Check if there's an output
if args.output:
    outName = args.output

# Check if wFrames is a number
if args.wframes:
    wFrames = args.wframes
try:
    wFrames=int(wFrames)
except ValueError:
    print "Oops! That's not a valid number. Please enter a valid number for the number of frames per slice.\n"
    while type(wFrames != int):
        try:
            wFrames=int(raw_input("Enter the number of frames per slice: \n"))
        except ValueError:
            print "Oops! That's not a valid number. Please enter a valid number for the number of frames per slice.\n"

# Checks if the file is indeed there - and if it isn't, browse your directories
if args.file:
    trajectory = args.file
if os.path.isfile(trajectory):
    if len(trajectory) < 4 or (len(trajectory)) >= 4 and trajectory[-4:] != ".dcd":
        print "Wrong trajectory name ! Your trajectory must be a .dcd file. Which file do you want ?"
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        trajectory = askopenfilename()
        while len(trajectory) < 4 or (len(trajectory)) >= 4 and trajectory[-4:] != ".dcd":
            trajectory = askopenfilename()

# Checks if the topology file is there
if args.psf:
    trajectory = args.psf
if os.path.isfile(psf):
    if len(psf) < 4 or (len(psf) >= 4 and psf[-4:] != ".psf"):
        print "Wrong topology name ! Your topology must be a .psf file. Which file do you want ?"
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        psf = askopenfilename()
        while len(psf) < 4 or (len(psf) >= 4 and psf[-4:] != ".psf"):
            psf = askopenfilename()

if args.gromacs:
    gromacs = True

######################## Functions ########################

def getNumframes(trajectory):
    """Gets the number of frames"""

    import MDAnalysis
    mobile = MDAnalysis.Universe(psf, trajectory)

    return mobile.trajectory.numframes

def makeSlice(trajectory, outName, directory, numFrames, wFrames, position):
    """Recursion to slice the trajectory into bits"""

    if numFrames-position>wFrames:
        output = directory + outName + "_" + str(position) + "-" + str(position + wFrames -1) + ".dcd"
    else:
        output = directory + outName + "_" + str(position) + "-" + str(numFrames) + ".dcd"

    bashCommand = catdcd_loc + " -o " + output + " -first " + str(position) + " -last " + str(position + wFrames - 1) + " " + trajectory
    subprocess.Popen(bashCommand, shell=True).wait()
    print bashCommand

    if wFrames+position>numFrames:
        sys.exit()

    return makeSlice(trajectory, outName, directory, numFrames, wFrames, position + wFrames)

def makeTrrSlice(trajectory, outName, directory, numFrames, wFrames, position)
    """Recursion to slice the trr"""

    if numFrames-position>wFrames:
        output = directory + outName + "_" + str(position) + "-" + str(position + wFrames -1) + ".trr"
    else:
        output = directory + outName + "_" + str(position) + "-" + str(numFrames) + ".trr"

    bashCommand = "gmx trjconv -o " + output + " -f " + trajectory + " -b " + str(position) + " -e " + str(position + wFrames -1)
    subsprocess.Popen(bashCommand, shell=True).wait()
    print bashCommand

    if wFrames+position>numFrames:
        sys.exit()

    return makeTrrSlice(trajectory, outName, directory, numFrames, wFrames, position + wFrames)

######################## Main ########################

if __name__ == '__main__':

    # If the max number of frames is in the command line, use it, else go fetch it in the trajectory with MDAnalysis
    if args.numframes:
        numFrames = args.numframes
    else:
        numFrames = getNumframes(trajectory)

    if gromacs == False:
        makeSlice(trajectory, outName, directory, numFrames, wFrames, 0)
    else:
        makeTrrSlice(trajectory, outName, directory, numFrames, wFrames, 0)












