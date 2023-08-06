#!/usr/bin/perl
#--------------------------------------------------------------------------
# Script: UpgradeVn.pl
#
# Author: Rosalyn Hatcher
#
# Description: This script takes each .check file in the $TEST_FILES_DIR
#              directory and updates the CF Checker version and 
#              Standard Name Table version in the file.
#
# Synopsis: ./UpgradeVn.pl
#
#           Before running simply alter the variables $checkerVN and
#           $standardNameVN as appropriate.
#-------------------------------------------------------------------------- 
$checkerVN="2.0.2";
$standardNameVN="16 (2010-10-11T12:16:51Z)";

$TEST_FILES_DIR="/home/ros/cf-checker/trunk/test_files";
chdir $TEST_FILES_DIR or die "Failed to cd to $TEST_FILES_DIR: $!\n";

foreach $file (<*.check>) {
    print "Upgrading $file...";

    open(CHECK,"$file") || warn "Cannot open file $file: $!";

    @new_file = ();

    while(<CHECK>) {
	if (/Using CF Checker Version/) {
	    push (@new_file, "Using CF Checker Version $checkerVN\n");
	} elsif (/Using Standard Name Table/) {
	    if ($file eq "stdName_test.check") {
		# Don't update the version of the Standard Name Table for this file
		push (@new_file, "$_");
	    } else {
		push (@new_file, "Using Standard Name Table Version $standardNameVN\n");
	    }
	} else {
	    push (@new_file, "$_");
	}
    }
    close(CHECK);

    # Write out new file
    open (NEW_FILE, "> $file.new") || warn "Cannot open file $file.new: $!";
    foreach $line (@new_file) {
	print NEW_FILE "$line";
    }
    close(NEW_FILE);

    rename ("$file.new", "$file") || warn "Failed to rename file: $!";
    print "    Done.\n";
}
