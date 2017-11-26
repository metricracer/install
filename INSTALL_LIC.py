#! /usr/bin/python

import glob, os, datetime, shutil, pwd, grp

todaysdate = datetime.datetime.today().strftime('%Y%m%d')
license_dir = "/opt/flexlm/licenses"
new_lic_dir = "/root/new_lic/20171116/*.lic"

## Make the save directory based on todays date
old_lic_sav_dir = "/root/old_lic/" + todaysdate
print("Making the license save directory based on todays date:" + old_lic_sav_dir)
if not os.path.exists(old_lic_sav_dir):
    print("    Creating directory: " + old_lic_sav_dir)
    os.makedirs(old_lic_sav_dir)
else:
    print("    Directory already exists: " + old_lic_sav_dir)

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
    print("    Copying new license: " + basename + " -> " + license_dir)
    shutil.copy2(fname, license_dir)
    print("    Changing ownership to flexlm: " + license_dir+"/"+basename)
    uid = pwd.getpwnam("flexlm").pw_uid
    gid = grp.getgrnam("root").gr_gid
    os.chown(license_dir+"/"+basename, uid, gid) 

    print("")
print("Done")
