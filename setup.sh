cd /tmp
rm -rf ./license ./old_lic ./new_lic
mkdir ./license ./old_lic ./new_lic

touch ./license/2016_aaaa.lic
touch ./license/2016_bbbb.lic
touch ./license/2016_cccc.lic
touch ./license/2016_dddd.lic

touch ./new_lic/2017_bbbb.lic
echo "some junk" >> ./new_lic/2017_bbbb.lic 
echo "some junk" >> ./new_lic/2017_bbbb.lic 
echo "some macminiserver junk" >> ./new_lic/2017_bbbb.lic 
echo "some more junk 1700" >> ./new_lic/2017_bbbb.lic 
echo "some junk" >> ./new_lic/2017_bbbb.lic 
