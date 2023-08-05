#!/usr/bin/env python
'''
From the main directory of a given ROOT file,
copy directory contents to new ROOT files.

That is, if example.root contains
    folderA
    folderB
    folderC...
then coopy contents of those folders to
    folderA.root
    folderB.root
    folderC.root...etc
'''
import sys
import os
from ROOT import TFile, TH1, TDirectory, gDirectory

def copy_to_new_tfile(in_tfile, out_tfile, full_path):
    '''Recursive function to copy all contents in a given directory
    in a given ROOT file to new ROOT file'''
    keys = in_tfile.GetDirectory(full_path).GetListOfKeys()
    for key in keys:
        name = key.GetName()
        classname = key.GetClassName()
        if 'TDirectory' in classname:
            #print "  %s/" % name
            gDirectory.mkdir(name)
            gDirectory.cd(name)  # go to new dir
            copy_to_new_tfile(in_tfile, out_tfile, '/'.join([full_path,name]))
            gDirectory.cd("..")  # come back from new dir
        else:
            #print "  %s" % '/'.join([full_path,name])
            hist = in_tfile.Get('/'.join([full_path,name]))
            hist.Write()

def split_file(filename):
    '''Find directories in the main dir, and copy contents to new ROOT files'''
    tfile = TFile(filename, "read")
    keys = tfile.GetDirectory('').GetListOfKeys()
    for key in keys:
        name = key.GetName()
        classname = key.GetClassName()
        if 'TDirectory' in classname:
            new_filename = '_'.join([filename[:-5],name]) + ".root"
            new_tfile = TFile(new_filename, "recreate")
            print "%18s/*  ->  %s" % (name, new_filename)
            copy_to_new_tfile(tfile, new_tfile, name)
            new_tfile.Close()
    tfile.Close()

def main():
    if len(sys.argv) < 1:
        print "Use:"
        print "rootsplit file.root"
        sys.exit(0)
    for filename in sys.argv[1:]:
        if not ".root" in filename:
            print "%s not a root file" % filename
            continue
        if not os.path.exists(filename):
            print "%s does not exist." % filename
            sys.exit(0)
        split_file(filename)

if __name__ == '__main__':
    main()
