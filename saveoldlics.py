#! /usr/bin/python

import glob, os, datetime, shutil

todaysdate = datetime.datetime.today().strftime('%Y%m%d')
license_dir = "/opt/flexlm/licenses"
new_lic_dir = "/root/new_lic/sep17/*.lic"

old_lic_sav_dir = "/root/old_lic/" + todaysdate
if not os.path.exists(old_lic_sav_dir):
    os.makedirs(old_lic_sav_dir)

for fname in glob.glob(new_lic_dir):
    #print(fname)
    dirlist = fname.split("/")
    #print(a)
    basename = dirlist[-1]
    #print(b)
    fnamelist = basename.split("_", 1)
    filenamewodate = fnamelist[-1]
    os.chdir("/opt/flexlm/licenses")
    for oldfile in glob.glob("*" + filenamewodate):
        print(oldfile)
	shutil.copy2(oldfile, old_lic_sav_dir)
