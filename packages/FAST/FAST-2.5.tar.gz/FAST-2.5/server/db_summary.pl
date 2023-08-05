#!/usr/bin/perl
#
# Stefan Chakerian (schake@sandia.gov)
# Sandia National Labs
# Jan, 2005
#
# This summarizes xml and output files from the webspace.
#
#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________
#

use POSIX;
use Data::Dumper;
use XML::Simple;
use URI::Escape;
use File::Copy;

#my ($curname, @dirlist, $xml, $i, $j, $webdir, $result, $interactive, $outfile);
#my ($cdate,$ctime,$cwho,$chost,$ccat,$cfile);
#my ($site, $tsite, $type, $dstat, $software, $estat, $istat);
#my ($percent, $total, $skipped, $status);
#my (%buildfail); # site/date/software hash
#my @errors;	# list of non-fatal errors to print at bottom
#local %world;
#local %packages;

#
# generic setup
# 
$ENV{PATH} = "/bin:/usr/bin:" . $ENV{PATH};
umask 002;


sub print_help {
  print "\n";
  print "db_summary [--help] [--html] [--install] <project-id> <project-name> [<*.xml>]\n";
  print "\n";
}

sub get_scenario {
  my $xml = shift;

  local $scenario="unknown-unknown";
  if (defined($xml->{Key}->{Scenario})) {
     $scenario = $xml->{Key}->{Scenario};
  } elsif (defined($xml->{Data}[0]->{Key}->{Scenario})) {
    $scenario = $xml->{Data}[0]->{Key}->{Scenario};
  } elsif (defined($xml->{Experiment}[0]->{Key}->{Scenario})) {
    $scenario = $xml->{Experiment}[0]->{Key}->{Scenario};
  }
  ;
  #print "scenario $scenario ->";
  @a = split /-/, $scenario;
  if (@a[2] eq "app") {
     $scenario = "app-" . @a[3];
  } else {
     $scenario = @a[1];
  }
  #if ($scenario =~ /^([^-]*)-([^-]*)-(.*)/) {
     #print "#1 $1 #2 $2\n";
     #$scenario = $2;
     #}
  #print "$scenario\n";

  return $scenario;
}

##
## MAIN
##
#
# Commandline args:
#	use arguments as data files, or else read $webdir/$framework/$date/*.xml
#
$install=0;
$html=0;
if (scalar(@ARGV) == 0) {
   print_help();
   exit(1);
} else {
  $tmp = shift @ARGV;
  if ($tmp eq "--help") {
     print_help();
     exit(1);
     }
  if ($tmp eq "--html") {
     $html=1;
     $tmp = shift @ARGV;
     }
  if ($tmp eq "--install") {
     $install=1;
     $tmp = shift @ARGV;
     }
  $framework=$tmp;
  $fname = shift @ARGV;
}
$interactive = scalar(@ARGV);
#
# Figure out the webspace directory
#
my $webroot="/home/sqe/public_html/testdata/$framework";
my $weburl="http://software.sandia.gov/~sqe/testdata/$framework";
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)= localtime(time);
$webdir = sprintf "%4d%02d%02d", $year+1900, $mon + 1, $mday;
#$webdir = "20051220";
if (!(-d "$webroot/$webdir" && -w "$webroot/$webdir" )) {
   die "Missing directory $webroot/$webdir\n";
}

##
## PARSE XML FILES
##
#
# Get the list of XML files
#
$dirname = "$webroot/$webdir";
if ($interactive > 0) {
  @dirlist = grep /\.xml$/, @ARGV;
  $dirname = '';
} else {
  opendir DATADIR, ($dirname) or die "opendir $dirname failed";
  @dirlist = grep /\.xml$/, readdir DATADIR;
  closedir DATADIR;
}
#
# Read in the XML files
#
foreach $curname (@dirlist) {
  #
  # Split the filenames into convenient pieces
  #
  ($cdate,$ctime,$cwho,$chost,$ccat,$cfile) = split /#/, $curname;
  #
  # Figure out the type of the file
  #
  $_ = $curname;
  if (/config/) {
    $type = "config";
  } elsif (/build/) {
    $type = "build";
  } elsif (/results/) {
    $type = "results";
  } elsif (/test/) {
    $type = "tests";
  } elsif (/scenario/) {
    $type = "scenario";
  } elsif (/check/) {
    $type = "check";
  } else {
    push @errors, "\"$curname\" does not contain [config|build|test|scenario|check] - skipping\n";
    next;
  }
  #
  # Ignore these types of files.
  #
  if ($type eq "check") {
     next;
  }
  #
  # $xmlfile contains the complete pathname of the file
  #
  #print "processing $curname...\n";
  if ($interactive) {
    $xmlfile = $curname;
  } else {
    $xmlfile = $dirname . "/" . $curname;
  }
  #
  # Parse the XML file
  #
  eval {
    $xml = XMLin("$xmlfile", forcearray => [ qw(Data Experiment Test) ] );
    };
  if ($@) {
    chomp $@;
    push @errors, "skipping $curname... (Bad XML format) $@\n";
    next;
    }
  #
  # Get the Scenario Key from the XML data structure
  #
  if (defined($xml->{Key})) {
    $site = $xml->{Key}->{HostName};
  } elsif (defined($xml->{Data}[0]{Key})) {
    $site = $xml->{Data}[0]->{Key}->{HostName};
  } elsif (defined($xml->{Experiment}[0]{Key})) {
    $site = $xml->{Experiment}[0]->{Key}->{HostName};
  } else {
    push @errors, "skipping $curname... (no <Key> found, check xml)\n";
    next;
  }
  if ($site eq "") {
     push @errors, "skipping $curname... (empty Scenario name, check xml)\n";
     next;
  }
  #
  # Get the scenario name
  #
  $scenario = get_scenario($xml);
  #
  # Setup the per-site dictionaries
  #
  $world{$site}{$type}[++$#{$world{$site}{$type}}]{filename} = "$curname";
  $world{$site}{$type}[$#{$world{$site}{$type}}]{xml} = $xml;
  #
  # Setup the per-scenario dictionaries
  #
  $packages{$scenario}{$type}[++$#{$packages{$scenario}{$type}}]{filename} = "$curname";
  $packages{$scenario}{$type}[$#{$packages{$scenario}{$type}}]{xml} = $xml;
}

##
## COLLECT STATISTICS
##
#
#	gather config and build summaries
#	move failure output files to webspace
#	unlink success output files, except when interactive
#
$nconfig_failures=0;
$nconfig_pfailures=0;
$nconfigs=0;
$nbuild_failures=0;
$nbuild_pfailures=0;
$nbuilds=0;
$ntest_failures=0;
$ntest_pfailures=0;
$ntests=0;
#
# Collect per-site statistics 
for $site (keys %world) {
  #
  # Config/Build statistics
  #
  for $type ("config","build") {
    $world{$site}{Pass}{$type} = 0;
    $world{$site}{Fail}{$type} = 0;
    for $i (0 .. $#{$world{$site}{$type}} ) {
      $estat = $world{$site}{$type}[$i]{xml}->{ExecutionStatus};
      $istat = $world{$site}{$type}[$i]{xml}->{IntegrityStatus};

      $curname = $world{$site}{$type}[$i]{filename};
      ($cfile = $curname) =~ s/xml$/out/;

      if ($type eq "config") {
      $nconfigs++;
      }
      else {
      $nbuilds++;
      }
      if ($estat eq "Pass" && $istat eq "Pass") {
	$world{$site}{Pass}{$type}++;
	#
	# Remove *.out files if there are no errors in these files
	#
	unlink "$dirname/$cfile" if (! $interactive);
      } else {
	if ($type eq "config") {
	   $nconfig_failures++;
	}
	else {
	   $nbuild_failures++;
	}
	$world{$site}{Fail}{$type}++;
      }
    }
  }
  #
  # Test statistics
  #
  for $type ("tests") {
    $world{$site}{Pass}{$type} = 0;
    $world{$site}{Fail}{$type} = 0;
    for $i (0 .. $#{$world{$site}{$type}} ) {
      $tmp = $world{$site}{$type}[$i]{xml}{Test};
      for $id (keys %$tmp) {
	$ntests++;
	$stat = $world{$site}{$type}[$i]{xml}{Test}{$id}{Status};
	if ($stat eq "Pass") {
	  $world{$site}{Pass}{$type}++;
	} else {
	  $ntest_failures++;
	  $world{$site}{Fail}{$type}++;
	}
      }
    }
  }
}
#
# Collect per-scenario statistics
#
for $scenario (keys %packages) {
  #
  # Config/Build statistics
  #
  for $type ("config","build") {
    $packages{$scenario}{Pass}{$type} = 0;
    $packages{$scenario}{Fail}{$type} = 0;
    for $i (0 .. $#{$packages{$scenario}{$type}} ) {
      $estat = $packages{$scenario}{$type}[$i]{xml}->{ExecutionStatus};
      $istat = $packages{$scenario}{$type}[$i]{xml}->{IntegrityStatus};
      if ($estat eq "Pass" && $istat eq "Pass") {
	$packages{$scenario}{Pass}{$type}++;
      } else {
	$packages{$scenario}{Fail}{$type}++;
      }
    }
  }
  #
  # Test statistics
  #
  for $type ("tests") {
    $packages{$scenario}{Pass}{$type} = 0;
    $packages{$scenario}{Fail}{$type} = 0;
    for $i (0 .. $#{$packages{$scenario}{$type}} ) {
      $tmp = $packages{$scenario}{$type}[$i]{xml}{Test};
      for $id (keys %$tmp) {
	$stat = $packages{$scenario}{$type}[$i]{xml}{Test}{$id}{Status};
	if ($stat eq "Pass") {
	  $packages{$scenario}{Pass}{$type}++;
	} else {
	  $packages{$scenario}{Fail}{$type}++;
	}
      }
    }
  }
}
##
## TODO
##
$nprojects = 0;
for $software (sort keys %packages) {
  if ($packages{$software}{Fail}{"config"} > 0) {
     $nconfig_pfailures++;
  }
  if ($packages{$software}{Fail}{"build"} > 0) {
     $nbuild_pfailures++;
  }
  if ($packages{$software}{Fail}{"tests"} > 0) {
     $ntest_pfailures++;
  }
  $nprojects++;
}
#
# Generate the test summary output file
#
open TESTSUMMARY, ">$framework/db_summary.txt" || die "ERROR: cannot open $framework/db_summary.txt";
if ($nconfigs==0) { $config_percent=0; }
   else { $config_percent=(100-ceil(100*$nconfig_failures/$nconfigs)); }
if ($nbuilds==0) { $build_percent=0; }
   else { $build_percent=(100-ceil(100*$nbuild_failures/$nbuilds)); }
if ($ntests==0) { $test_percent=0; }
   else { $test_percent=(100-ceil(100*$ntest_failures/$ntests)); }

if ($nconfigs==0) { $proj_config_percent=0; }
   else { $proj_config_percent = (100-ceil(100*$nconfig_pfailures/$nprojects)); }
if ($nbuilds==0) { $proj_build_percent=0; }
   else { $proj_build_percent=(100-ceil(100*$nbuild_pfailures/$nprojects)); }
if ($ntests==0) { $proj_test_percent=0; }
   else { $proj_test_percent=(100-ceil(100*$ntest_pfailures/$nprojects)); }

$testsummary = sprintf("(%3d/%3d/%3d)  [%3d/%3d/%3d]", $config_percent, $build_percent, $test_percent, $proj_config_percent, $proj_build_percent, $proj_test_percent);
printf TESTSUMMARY "%s\n",$testsummary;
close(TESTSUMMARY);

if ($html) {
   open SUMMARY, ">$framework/summary.html" || die "ERROR: cannot open $framework/summary.html";
} else {
   open SUMMARY, ">$framework/summary.txt" || die "ERROR: cannot open $framework/summary.txt";
}
##
## PRINT REPORT
##
$mydate = `date`;
chomp $mydate;
       #0123456789012345678901234567890123456789012345678901234567890123456789012345
if ($html) {
   printf SUMMARY "<body>\n";
   printf SUMMARY "<pre>\n";
}
printf SUMMARY "******************************** SQA REPORT ********************************\n";
printf SUMMARY "****************************************************************************\n";
$foo = $fname . " " . $testsummary;
printf SUMMARY " %-41.41s   %30.30s\n", $foo, $mydate;
#printf SUMMARY " %-25.25s   %s   %30.30s\n", $framework, $testsummary, $mydate;
printf SUMMARY "****************************************************************************\n";
printf SUMMARY "****************************************************************************\n";
#
# Print summary statistics
#
printf SUMMARY "\nSUMMARY: Config/Build/Test Results by Test Machine             (NFail/Total)\n";
printf SUMMARY "----------------------------------------------------------------------------\n";
printf SUMMARY "Machine                        OS                Config    Build      Test\n";
printf SUMMARY "----------------------------------------------------------------------------\n";
for $site (sort keys %world) {
  my $arch = 'UNKNOWN';
  $arch = $world{$site}{config}[0]{xml}{Key}{KernelName};

  printf SUMMARY "%-30.30s %-15.15s", $site, $arch;
  for $type ("config","build","tests") {
    my $total = $world{$site}{Pass}{$type} + $world{$site}{Fail}{$type};
    if ($world{$site}{Fail}{$type} == 0) {
       printf SUMMARY "    ./%-4d", $total;
    } else {
       printf SUMMARY " %4d/%-4d", $world{$site}{Fail}{$type},$total;
    }
  }
  $---;			# decrement format page count
  printf SUMMARY "\n";
}
#
# Print scenario statistics
#
printf SUMMARY "\n\nSUMMARY: Config/Build/Test Results by Test Package             (NFail/Total)\n";
printf SUMMARY "----------------------------------------------------------------------------\n";
printf SUMMARY "Package                        Coverage          Config    Build      Test\n";
printf SUMMARY "----------------------------------------------------------------------------\n";
for $software (sort keys %packages) {
  printf SUMMARY "%-30.30s %-15.15s", $software, "NA";
  for $type ("config","build","tests") {
    my $total = $packages{$software}{Pass}{$type} + $packages{$software}{Fail}{$type};
    if ($packages{$software}{Fail}{$type} == 0) {
       printf SUMMARY "    ./%-4d", $total;
    } else {
       printf SUMMARY " %4d/%-4d", $packages{$software}{Fail}{$type},$total;
    }
  }
  $---;			# decrement format page count
  printf SUMMARY "\n";
}
#
# Format output lines
#
$~ = 'SUMMARY';
select SUMMARY;
if ($html) {
   $pre="</pre>"
} else {
   $pre = ""
}
format SUMMARY =
@<<<<<<<<<<<<<<< @>>>>>>>>> @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  @<<<<<<<<<<<<<< @<<<<<
$tsite,          $dstat,    $software,                      $status,        $pre
.

#
# Print config/build errors
#
print "\n\nFAILURES: Config/Build\n";
print "----------------------------------------------------------------------------\n";
print "Host             Date       Scenario                        Status\n";
print "----------------------------------------------------------------------------$pre\n";

$flag=0;
for $site (sort keys %world) {
  for $type ("config","build") {
    for $i (0 .. $#{$world{$site}{$type}} ) {
      $dstat = $world{$site}{$type}[$i]{xml}->{Key}->{Date};
      $software = $world{$site}{$type}[$i]{xml}->{Key}->{Scenario};
      #$dstat = $world{$site}{$type}[$i]{xml}->{Data}[0]->{Key}->{Date};
      #$software = $world{$site}{$type}[$i]{xml}->{Data}[0]->{Key}->{Scenario};
      $estat = $world{$site}{$type}[$i]{xml}->{ExecutionStatus};
      $istat = $world{$site}{$type}[$i]{xml}->{IntegrityStatus};
      if ($estat ne "Pass") {
        $status = "Error";
      } elsif ($istat ne "Pass") {
	$status = "Fail";
      } else {
	$status = "Pass";
      }
      if ($status ne "Pass") {
	$tsite = $site;	# protection vs write side-effects
        @a = split(/-/, $software);
	shift @a;
	$software = join("-",@a);
        $curname = $world{$site}{$type}[$i]{filename};
	($cfile = $curname) =~ s/xml$/out/;
	if ($html) {
           print "<a href=\"$weburl/$webdir/" . uri_escape($cfile) . "\"><pre>";
	   write;
           print "</a>\n";
	} else {
	   write;
           print "$weburl/$webdir/" . uri_escape($cfile) . " \n";
	}
	#
        # don't print test results in lower section for failed build
	#
	# this will give problems if multiple tests run on same day and output
	# was committed to repository.  Any build failure will suppress test
	# output, even if a subsequent build worked.  The only way around this
	# is to run with recent build files, interactively (command-line args)
	#
	$buildfail{$site}{$dstat}{$software} = 1;
        $--- if ($- > 0);
	$flag=1;
      }
    }
  }
}
if ($html) {
   printf "<pre>\n";
}
if ($flag == 0) {
   printf "None$pre\n";
   printf "<pre>\n";
   }
#
# Print config/build errors
#
printf "\n\nFAILURES: Tests\n";
printf "----------------------------------------------------------------------------\n";
printf "Host             Date       Scenario                        Status\n";
printf "                                                            %%Good/#Err/Total\n";
printf "----------------------------------------------------------------------------$pre\n";

$flag=0;
for $site (sort keys %world) {
  for $type ("tests") {
    my %h;
    my $skipped=0;
    for $i (0 .. $#{$world{$site}{$type}} ) {
      my $passed = 0;
      $tmp = $world{$site}{$type}[$i]{xml}{Test};
      $estat = 0;
      for $id (keys %$tmp) {
	$istat = $world{$site}{$type}[$i]{xml}{Test}{$id}{Status};
        $passed++ if ($istat eq "Pass");
        $estat = $estat + 1;
      }
      $dstat = $world{$site}{$type}[$i]{xml}->{Data}[0]->{Key}->{Date};
      $software = $world{$site}{$type}[$i]{xml}->{Data}[0]->{Key}->{Scenario};
      $curname = $world{$site}{$type}[$i]{filename};
      $percent = ($estat - $skipped == 0) ? 100
		      : sprintf "%2d", 100.0*($passed / ($estat - $skipped));
      #
      # save data to be printed but don't write yet
      #
      $status = ($passed < ($estat - $skipped) );
      #printf "$dstat $software $percent $passed $estat $skipped $flag $status\n";
      push @{$h{ $software }}, ( {
	  "date" => "$dstat",
	  "software" => "$software",
	  "percent" => $percent,
	  "passed" => $passed,
	  "total" => $estat,
	  "skipped" => "$skipped",
	  "curname" => "$curname",
	} ) if ($passed < ($estat - $skipped) );
    }
    #
    # sort output by name, then write it out
    #
    for my $sware (sort keys %h) {
      $flag=1;
      for $i (0 .. $#{$h{$sware}}) {
	$software = $sware;
        @a = split /-/, $software;
	shift @a;
	$software = join("-",@a);
	$dstat = $h{$sware}[$i]{date};
	$percent = "$h{$sware}[$i]{percent}";
	$total = $h{$sware}[$i]{total};
	$curname = $h{$sware}[$i]{curname};
	$skipped = $h{$sware}[$i]{skipped};
	$sw = $h{$sware}[$i]{software};
	$passed = $h{$sware}[$i]{passed};
	$nerr = $total - $passed;
	$status = sprintf '%3s%% /%4d/%4d', $percent, $nerr, $total;
	$tsite = $site;	# protection vs write side-effects
        #
        # no use showing failed tests if the build failed earlier
        # (bah, this should be up above.)
	#
 	if (!$buildfail{$site}{$dstat}{$sw}) {
	   if ($html) {
              print "<a href=\"$weburl/$webdir/" . uri_escape($curname) . "\"><pre>";
 	      write;
	      print "</a>\n";
	   } else {
 	      write;
              print "$weburl/$webdir/" . uri_escape($curname) . " \n";
           }
        }
      }
    }
  }
}
if ($html) {
   printf "<pre>\n";
}
if ($flag == 0) {
   print "None$pre\n";
   }

# print any non-fatal errors from above at end
if (scalar(@errors)) {
  print "\n\nFAILURES: Bad Input Files\n";
  print "----------------------------------------------------------------------------\n";
  print @errors;
}

if ($html) {
   print "</pre>\n";
   print "</body>\n";
}
close(SUMMARY);

if ($install == 1) {
   if ($html) {
      copy("$framework/summary.html","$webroot/$webdir");
   } else {
      copy("$framework/summary.txt","$webroot/$webdir");
   }
   if (-e "$webroot\/today") {
      unlink "$webroot\/today";
      }
   symlink("$webroot\/$webdir", "$webroot\/today");
   }
