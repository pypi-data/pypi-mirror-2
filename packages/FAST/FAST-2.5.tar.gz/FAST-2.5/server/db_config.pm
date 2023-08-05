#!/usr/bin/perl
#
# William Hart (wehart@sandia.gov)
# Sandia National Labs
# March, 2006
#
# This configuration file defines the software projects that are managed
# by the DB Server.
#
# Note: these configuration options define operations that will be executed
# 	at the db-server directory.
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

$weburl="http://software.sandia.gov/~sqe/testdata/$framework";
$webroot  = "/home/sqe/public_html/testdata";
$cvs_root = "/space/sandiacvs/CVS-FAST";

%db_config = (
   #
   # The Acro optimization library
   #
#   'acro' => {
#	name => 'Acro',
#	maillist => 'acro-regression@software.sandia.gov',
#	},
   #
   # The TEVA libraries
   #
   #'teva' => {
#	name => 'TEVA',
#	maillist => 'teva-tests@listserv.uc.edu wehart@sandia.gov jberry@sandia.gov',
#	},
   #
   # Zoltan
   #
   'zoltan' => {
	name => 'Zoltan',
	maillist => 'zoltan-regression@software.sandia.gov wehart@sandia.gov',
	},
   #
   # Dakota
   #
#   'dakota' => {
#	name => 'Dakota',
#	maillist => 'jdsiiro@sandia.gov wehart@sandia.gov briadam@sandia.gov mseldre@sandia.gov',
#	},
   #
   # COIN
   #
   #'coin' => {
#	name => 'Coin',
#	maillist => 'wehart@sandia.gov',
#	},
   #
   # EPANET
   #
   #'epanet' => {
	#name => 'EPANET',
	#maillist => 'wehart@sandia.gov jim.uber@uc.edu',
	#},
   #
   # AutoDock
   #
   #'autodock' => {
	#name => 'AutoDock',
	#maillist => 'wehart@sandia.gov',
	#},
   #
   # Dimension Reduction
   #
   #'dimred' => {
	#name => 'DimRed',
	#maillist => 'jwatson@sandia.gov',
	#},
);

$val = 0;
$cvs_update = "cvs -Q -d $cvs_root update -d data";
$cvs_checkout = "cvs -Q -d $cvs_root checkout data";
$cvs_remove = "cvs -d $cvs_root remove";
$cvs_commit = "cvs -d $cvs_root commit -m \"Files removed by the FAST db-daemon\" data";

1;
