#!/bin/ksh
#

#cd Test_Files

outdir=tests_output.$$
mkdir $outdir

export PYTHONPATH=/home/ros/software/python/cdat-lite:/home/ros/software/python/udunits
std_name_table=http://cf-pcmdi.llnl.gov/documents/cf-standard-names/standard-name-table/current/cf-standard-name-table.xml
area_table=http://cf-pcmdi.llnl.gov/documents/cf-standard-names/area-type-table/current/area-type-table.xml

# Testing w/ CDAT-5.2 and UDUNITS2
export PYTHONPATH=/home/ros/software/CDAT-5.2-cdms/bin
export LD_LIBRARY_PATH=/home/ros/software/udunits2/lib
export UDUNITS=/home/ros/software/udunits2/share/udunits/udunits2.xml

# udunits-2.1.19
export LD_LIBRARY_PATH=/home/ros/software/udunits-2.1.19/lib
export UDUNITS=/home/ros/software/udunits-2.1.19/share/udunits/udunits2.xml

cfchecker="../src/cfchecker/cfchecks.py"

failed=0

for file in `ls *.nc`
do
  if test $file == "badc_units.nc"
  then
    # Check --badc option (Note:  Need to set path to badc_units.txt in cfchecks.py)
    $cfchecker --badc $file -s $std_name_table > $outdir/$file.out 2>&1
  elif test $file == "stdName_test.nc"
  then
    # Check --cf_standard_names option
    $cfchecker -s ./stdName_test_table.xml -a $area_table $file > $outdir/$file.out 2>&1
  elif test $file == "CF_1_2.nc"
  then
    # CF-1.2
    $cfchecker -s $std_name_table -v 1.2 $file > $outdir/$file.out 2>&1
  elif test $file == "flag_tests.nc"
  then
    # CF-1.3
    $cfchecker -s $std_name_table -v 1.3 $file > $outdir/$file.out 2>&1
  elif [[ $file == "Trac049_test1.nc" || $file == "Trac049_test2.nc" ]]
  then 
    # CF-1.4
    $cfchecker -s $std_name_table -a $area_table -v 1.4 $file > $outdir/$file.out 2>&1
  else
    # Run the checker on the file
    $cfchecker -s $std_name_table -v 1.0 $file > $outdir/$file.out 2>&1
  fi
  # Check the output against what is expected
  result=${file%.nc}.check
  diff $outdir/$file.out $result >/dev/null
  if test $? == 0
  then
    echo $file: Success
    rm $outdir/$file.out
  else
    echo $file: Failed
    #rc=$((failed += 1))
    failed=`expr $failed + 1`
  fi
done

# Print Test Results Summary
echo ""
if [[ $failed != 0 ]]
then
  echo "****************************"
  echo "***    $failed Tests Failed    ***"
  echo "****************************"
else
  echo "****************************"
  echo "*** All Tests Successful ***"
  echo "****************************"
fi

# Check that the script options

# --cf_standard_names

# --udunits

# --coards


