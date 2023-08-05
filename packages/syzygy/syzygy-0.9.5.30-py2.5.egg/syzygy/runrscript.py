#!/usr/bin/python

# Written by Manuel A. Rivas
# Updated 07.13.2009

# The Broad Institute
# SOFTWARE COPYRIGHT NOTICE AGREEMENT
# This software and its documentation are copyright 2009 by the
# Broad Institute/Massachusetts Institute of Technology. All rights are
# reserved.

# This software is supplied without any warranty or guaranteed support
# whatsoever. Neither the Broad Institute nor MIT can be responsible for its
# use, misuse, or functionality.
# $Header$
from optparse import OptionParser
from os import popen
from mpgutils import utils    
from mpgutils.RUtils import RscriptToPython
import optparse                                                                                                                                                                                               
import sys
import re
import os

def main(argv = None):
    if not argv:
        argv = sys.argv
#    lstRequiredOptions = ["targetfile", "poolinfofile","rarethr"]
    usage = "usage: %prog [options] "
    parser = optparse.OptionParser(usage)
    #REQUIRED Commands
    parser.add_option("--pif",
                      help = "Pool Info File")
    parser.add_option("--outputdir",
                      help = "Output Directory")
#===============================================================================
#    parser.add_option("--table_file_name",
#                      help = "table_file_name")
#    parser.add_option("--output_file_name",
#                      help = "output_file_name")
#    parser.add_option("--num_people",
#                      help = "Number of people")
#===============================================================================
    
    dctOptions, lstArgs = parser.parse_args(argv)
    
    #REQUIRED OPTIONS
    lstRequiredOptions=["pif"]
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    #**********************
    #IS THERE SOME WAY THAT WE COULD FIGURE OUT NUM_PEOPLE WITHOUT THE USER HAVING TO ENTER THIS INFORMATION IN?
    #*********************
    #MUST HAVE THE R LIBRARY INSTALLED PROPERLY, IF YOU CAN RUN R AND TYPE library("mpganalysis.syzygy") AND IT LOADS
    #THEN YOU SHOULD BE GOLDEN
    #**********************
    pifpath = open(dctOptions.pif,'r').readlines()
    for line in pifpath[1:]:
        line = line.rstrip()
        line = line.split()
        bamfile = line[0]
        individuals = line[2]
        table_file_name = str(bamfile) + '.combined.error.coverage'
        output_file_name = str(bamfile) + '.combined.error.coverage.calls'
        num_people = int(individuals)
        print num_people
        print '\n\n'
        CallonR(table_file_name,output_file_name,num_people)
       
def CallonR(table_file_name,output_file_name,num_people):
    lstLibraries=["mpganalysis.syzygy"]
    methodName="syzygylikelihoodcalc"
    
    #TABLE FILE NAME PATH
#===============================================================================
#    filePath = utils.ensurePath(table_file_name)
#    if filePath:
#        setattr(table_file_name, filePath)
#    else:
#        print "Cound not find " + table_file_name
#        sys.exit(2)
#    
#    #OUTPUT FILE NAME PATH
#    filePath = utils.ensurePath(output_file_name)
#    if filePath:
#        setattr(output_file_name, filePath)
#    else:
#        print "Cound not find " + output_file_name
#        sys.exit(2)
#    
#===============================================================================
    dctArguments={"table_file_name":table_file_name,
                  "output_file_name":output_file_name,
                  "num_people":num_people,
                  "verbose":True
                  }
    
    RscriptToPython.callRscript(lstLibraries, methodName, dctArguments, True)

if __name__ == "__main__":
    main()
    