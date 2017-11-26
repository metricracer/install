#! /usr/bin/python

import glob, os, datetime, shutil, pwd, grp
import re


class dirpath(object):
    ############################################################################
    def __init__(self, env_variable, datepath=""):
        try:
            envpath = os.environ[env_variable]
            self.name = envpath + datepath
        except KeyError:
            raise Exception('ENV variable: ' + env_variable + ' not set!')

        print("Making the license save directory:" + self.name)
        if not os.path.exists(self.name):
            print("    Creating directory: " + self.name)
            os.makedirs(self.name)
        else:
            print("    Directory already exists: " + self.name)


class dirpathdate(dirpath):
    ############################################################################
    def __init__(self, env_variable):
        todaysdate = datetime.datetime.today().strftime('%Y%m%d')
        datepath = "/" + todaysdate
        super(dirpathdate, self).__init__(env_variable, datepath)


####################################################################################
def for_this_host(lic_file):
    qname = os.uname()[1]
    qnamelst = qname.split(".")
    thishost = qnamelst[0]
    print("    Scanning license for current hostname: " + thishost)
    linecount = 0
    retVal = False
    for line in open(lic_file):
        if thishost in line:
            print("    License hostname verified: " + thishost)
            retVal = True
            break

        if (linecount > 5):
            print("    Incorrect hostname found in file: " + lic_file)
            retVal = False
            break

        linecount += 1

    if (linecount == 0):
        print("    License file appears empty: " + lic_file)
        retVal = False

    return retVal


####################################################################################
def main():
    ## Define license directory
    license_dir_obj = dirpath('LICENSE_DIR')

    ## Define initial location of new licenses
    new_license_dir_obj = dirpath('LICENSE_NEW_SAVE')

    ## Define new licenses search glob
    new_lic_glob = new_license_dir_obj.name + "/*.lic"

    ## Make the save directories based on todays date
    old_lic_sav_dir_obj = dirpathdate('LICENSE_OLD_SAVE')
    new_lic_sav_dir_obj = dirpathdate('LICENSE_NEW_SAVE')
    print("")

    ## Looping through all filenames in new_lic dir
    print("Looping through all license files in: " + new_lic_glob)
    print("")
    for fname in glob.glob(new_lic_glob):
       
        ## determine license name w/o date
        dirlist = fname.split("/")
        basename = dirlist[-1]
        fnamelist = basename.split("_", 1)
        filenamewodate = fnamelist[-1]

        print("    Found new license file: " + basename)

        ## Look for this hostname at top of license file
        if not (for_this_host(fname)):
            continue

        os.chdir(license_dir_obj.name)

        ## look for any old matching licenses ie. "*Petrel_Analytics.lic"
        print("    Searching license dir for any old license files that ends with: *" + filenamewodate)
        ## Copy and remove each one
        for oldfile in glob.glob("*" + filenamewodate):
            if (oldfile != basename):
                print("    Moving old license: " + oldfile + " -> " +
                        old_lic_sav_dir_obj.name)
                shutil.copy2(oldfile, old_lic_sav_dir_obj.name)
                os.remove(oldfile)

        ## Copy new license to licenses directory
        print("    Installing new license: " + basename + " -> " +
                license_dir_obj.name)
        shutil.copy2(fname, license_dir_obj.name)
        print("    Changing ownership to flexlm: " + license_dir_obj.name+"/"+basename)
        #uid = pwd.getpwnam("flexlm").pw_uid
        #gid = grp.getgrnam("root").gr_gid
        uid = pwd.getpwnam("darthvader").pw_uid
        gid = grp.getgrnam("admin").gr_gid
        os.chown(license_dir_obj.name+"/"+basename, uid, gid) 

        ## Move original license to save directory
        print("    Storing original license: " + fname + " -> " +
                new_lic_sav_dir_obj.name)
        shutil.copy2(fname, new_lic_sav_dir_obj.name)
        os.remove(fname)

        print("")
    print("Done")


if __name__ == "__main__":
    print("This only executes when %s is executed rather than imported" % __file__)
    main()
