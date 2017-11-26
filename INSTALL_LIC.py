#! /usr/bin/python

import glob, os, datetime, shutil, pwd, grp
import re

####################################################################################
def make_directory(lic_sav_dir):
    print("Making the license save directory based on todays date:" + lic_sav_dir)
    if not os.path.exists(lic_sav_dir):
        print("    Creating directory: " + lic_sav_dir)
        os.makedirs(lic_sav_dir)
    else:
        print("    Directory already exists: " + lic_sav_dir)

####################################################################################
def for_this_host(lic_file):
    thishost = os.uname()[1]
    linecount = 0
    for line in open(lic_file):
        if thishost in line:
            print("    License hostname verified: " + thishost)
            return True

        if (linecount > 5):
            print("    Incorrect hostname found in file: " + lic_file)
            return False

        linecount += 1


todaysdate = datetime.datetime.today().strftime('%Y%m%d')
license_dir = "/opt/flexlm/licenses"
new_lic_dir = "/root/new_lic/*.lic"

## Make the save directories based on todays date
old_lic_sav_dir = "/root/old_lic/" + todaysdate
new_lic_sav_dir = "/root/new_lic/" + todaysdate
make_directory(old_lic_sav_dir)
make_directory(new_lic_sav_dir)
print("")

## Looping through all filenames in new_lic dir
print("Looping through all license files in: " + new_lic_dir)
print("")
for fname in glob.glob(new_lic_dir):
   
    ## determine license name w/o date
    dirlist = fname.split("/")
    basename = dirlist[-1]
    fnamelist = basename.split("_", 1)
    filenamewodate = fnamelist[-1]

    print("    Found new license file: " + basename)

    ## Look for this hostname at top of license file
    if not (for_this_host(fname)):
        continue

    os.chdir(license_dir)

    ## look for any old matching licenses ie. "*Petrel_Analytics.lic"
    print("    Searching license dir for any old license files that ends with: *" + filenamewodate)
    ## Copy and remove each one
    for oldfile in glob.glob("*" + filenamewodate):
        if (oldfile != basename):
            print("    Moving old license: " + oldfile + " -> " + old_lic_sav_dir)
            shutil.copy2(oldfile, old_lic_sav_dir)
            os.remove(oldfile)

    ## Copy new license to licenses directory
    print("    Installing new license: " + basename + " -> " + license_dir)
    shutil.copy2(fname, license_dir)
    print("    Changing ownership to flexlm: " + license_dir+"/"+basename)
    uid = pwd.getpwnam("flexlm").pw_uid
    gid = grp.getgrnam("root").gr_gid
    os.chown(license_dir+"/"+basename, uid, gid) 

    ## Move original license to save directory
    print("    Storing original license: " + fname + " -> " + new_lic_sav_dir)
    shutil.copy2(fname, new_lic_sav_dir)
    os.remove(fname)

    print("")
print("Done")
