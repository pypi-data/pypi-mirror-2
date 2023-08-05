drop table if exists package;
drop table if exists subpackage;
drop table if exists param;
drop table if exists machine;
drop table if exists scenario;
drop table if exists artifact;
drop table if exists artnote;
drop table if exists file;
drop table if exists study;
drop table if exists analysis;
drop table if exists category;
drop table if exists tag;
drop table if exists tstatus;
drop table if exists experiment;
drop table if exists trial;
drop table if exists measurement;



# package will be relatively small.
# e.g. acro, zoltan, dimred
# name = experiment version
# fullname = formal name
# version = optional tags
# drop table if exists package;
CREATE TABLE if not exists package (
  package_id	smallint(3) unsigned not null auto_increment primary key,
  name          char(20),			# from <Key>
  fullname      varchar(60),			# guessed from <Key>
  version       varchar(20),			# updated manually
  contact	varchar(255),			# updated manually
  urlbase	varchar(255),			# updated manually
  urlhome	varchar(255)			# updated manually
);


# subpackage will index both itself, the package, and any extra arguments
# e.g. [acro]-subpackage-nightly would index subpackage and nightly
# Most queries will then be on subpackage based on a known package_id
# drop table if exists subpackage;
CREATE TABLE if not exists subpackage (
  subpackage_id int(3) unsigned not null auto_increment primary key,
  package_id	smallint unsigned not null,
  name		varchar(40) not null default "?",	# from <Key>

  index (package_id, subpackage_id)
);


# drop table if exists param;
CREATE TABLE if not exists param (
  param_id	int(3) unsigned not null auto_increment primary key,
  subpackage_id	int unsigned not null,
  name		varchar(40),				# from <Key>

  index (subpackage_id)
);


# machines
#
#     KernelName="Linux"
#     HostName="baley.sandia.gov"
#     KernelRelease="2.6.9-42.0.10.ELsmp"
#     KernelVersion="#1 SMP Fri Feb 16 17:13:42 EST 2007"
#     Machine="x86_64"
#     Processor="x86_64"
#     OS="Linux baley.sandia.gov 2.6.9-42.0.10.ELsmp #1 SMP Fri Feb 16 17:13:42 EST 2007 x86_64 x86_64 x86_64 GNU/Linux"
#     Scenario="dimred-lin64-gcc"
#     Date="2007-12-11 00:05:03"

# drop table if exists machine;
CREATE TABLE if not exists machine (
  machine_id    int(5) unsigned not null auto_increment primary key,
  host_name     varchar(100),
# if host changes hardware or kernel but keeps name, increment host_ver in new record
  host_ver      smallint(2) unsigned not null default 1,
  kernel_name   varchar(40),
  kernel_rel    varchar(100),
  kernel_ver    varchar(255),
  machine       varchar(255),
  processor     varchar(255),
  OSstring      varchar(255),
  location      varchar(255),		# optional, manual update
  description   varchar(255),		# optional, manual update
  update_time   timestamp		# creation/modification time
);



# scenarios contain info about the particular run
# such as host machine, and has the build info and
# the collection of studies
# drop table if exists scenario;
CREATE TABLE if not exists scenario (
  scenario_id   int(6) unsigned not null auto_increment primary key,
  package_id    smallint(3) unsigned not null default 0,
  subpackage_id int unsigned,
  param_id	int unsigned,
  machine_id    int(5) unsigned not null default 0,
  start_time    datetime,
  end_time      datetime,
  run_time      float(6,1) unsigned,
  param         varchar(255),		# extra tags
  path          varchar(255),
  branch_tag    varchar(255),
  build_dir     varchar(255),
  description   varchar(255),
  dependencies  text,
  commandline   text,
  update_time   timestamp,

  index (start_time),
  index (end_time),
  index (machine_id),
  index (package_id, subpackage_id, param_id)
);


# artifacts:
# This currently has build info and config info of a scenario.
# It also contains a status, which is is a throwback to
# the Exact datastructures, which should be redone to handle
# artifacts correctly.
# Artifact are unique by scenario/type.  One artifact can have
# multiple files, but they ALL must be under a single "file" artifact
# drop table if exists artifact;
CREATE TABLE if not exists artifact (
  artifact_id	int unsigned not null auto_increment primary key,
  scenario_id	int unsigned not null default 0,
  start_time	datetime,
  end_time	datetime,
  run_time	float(6,1) unsigned,
  status	ENUM("Fail", "Pass") null,
  status_exec	ENUM("Fail", "Pass") null,

# type is what kind of artifact.  Add others as desired
# e.g. config artifacts need the output file plus flags plus warnings
# while other artifacts might not have any attached notes
# There should probably be a user-defined type, or perhaps all
# types should be user-defined.
  type		ENUM("Error", "Config","Build","File") NOT NULL,

  index (scenario_id,type)
);


# artifact notes:
# currently these are the "warnings" and "flags" in the SoftwareInfo
# (config/build) nodes.
# zero or more artifactnotes per artifact
# Generalizing it, it is just a textual note and an associated type
# joined to an artifact.
# drop table if exists artnote;
CREATE TABLE if not exists artnote (
  artnote_id	int unsigned not null auto_increment primary key,
  artifact_id	int unsigned,
  type		ENUM("unknown", "flag", "warning") NOT NULL,
  data		text,

  index (artifact_id)
);


# file:
# file to join to a particular artifact
# zero or more files per artifact
# multiple artifacts per scenario possible
# drop table if exists file;
CREATE TABLE if not exists file (
  file_id       int unsigned not null auto_increment primary key,
  artifact_id   int unsigned,
  # add more filetypes as necessary
  type		ENUM("unknown", "XML", "Log", "Output",
		  "Study", "Analysis", "Results") NOT NULL,
  name		varchar(255),
  url           varchar(255),
  linkname	varchar(255),
# url should be from base directory, without http://www.domain.gov,
# which will be provided by the baseurl in the package table
# linkname is optional anchor to use instead of name

  index (artifact_id,type)
);


# a study is simply a list of experiments + analyses, and tags
# within a scenario
# drop table if exists study;
create table if not exists study (
  study_id	int unsigned not null auto_increment primary key,
  scenario_id	int unsigned,
  name		varchar(255) not null,

  index (scenario_id)
);


# analyses are interpreted results of an experiment:
# collection of trials + results of pass/fail
# this is the result of the tests (what the user is interested in)
#
# drop table if exists analysis;
create table if not exists analysis (
  analysis_id	int unsigned not null auto_increment primary key,
  study_id	int unsigned not null default 0,
  name		varchar(255),

# types are the registered analyses at the bottom of exact/analysis.py
# Append to this enum if you add others, or new ones will be "unknown"
# Do not insert new values into the middle of the enum,
# or it might break existing db entries!  (Need to verify mysql behavior)
  type		ENUM("validation", "relative_performance",
		"baseline", "lcov", "table") NULL,
  index (study_id)
# index (study_id, status)   not sure we need status here
);


# categories (for analyses)
# drop table if exists category;
create table if not exists category (
  category_id	int unsigned not null auto_increment primary key,
  analysis_id	int unsigned,
  name		varchar(255),
  index (analysis_id)
);


# tags (for studies)
# drop table if exists tag;
create table if not exists tag (
  tag_id	int unsigned not null auto_increment primary key,
  study_id	int unsigned,
  name		varchar(255),
  index (study_id)
);


# test status for analyses
# analyses have short status for each test
# analysis/tstatus corresponds (indirectly) to experiments/trials
# this table has some duplication of other tables, but so do the datastructures
# drop table if exists tstatus;
create table if not exists tstatus (
  tstatus_id	int unsigned not null auto_increment primary key,
  analysis_id	int unsigned,
  experiment	varchar(255),	# experiment_id would be better, eventually
  comb		varchar(20),	# id (normally integer, but treated as a string)
		# status should correspond to the similar experiment
  status	enum("Fail", "Pass") NOT NULL,
  index (analysis_id,experiment,comb)
);


##############
# Experiments are currently not being read in by Exact.
#
# The code to do it is not written in Exact, so the following tables
# aren't used.
############

# experiments are a collection of trials
# drop table if exists experiment;
create table if not exists experiment (
  experiment_id	int unsigned not null auto_increment primary key,
  study_id	int unsigned not null default 0,
  start_time	datetime,
  run_time	float(6,1) unsigned,
  status_exec	enum("Fail", "Pass") NOT NULL,	# exec status: did it run?
  name		varchar(255),
  id		varchar(20),
  category	varchar(255),
  description	text,

  index (study_id, status_exec)
);


# trials are collections of measurement results, exit comments, etc
# they compose an experiment
# drop table if exists trial;
create table if not exists trial (
  trial_id	int unsigned not null auto_increment primary key,
  experiment_id	int unsigned not null default 0,
  status_run	enum("Fail", "Pass") NOT NULL,

# id and seed are static measurements in every trial
  id		varchar(20),
  seed		float,

  index (experiment_id)

#   might want to tie to analyses... not sure yet
# analysis_id	int unsigned not null default 0,
# index (analysis_id)
);


# drop table if exists measurement;
create table if not exists measurement (
  measurement_id  int unsigned not null auto_increment primary key,
  trial_id	int unsigned not null default 0,
  experiment_id	int unsigned not null default 0,
  name		varchar(255),
# type was duplicated from Dart (sans encoding, compression)
# http://public.kitware.com/pipermail/dart/2001-September/000070.html
# only a few types are supported, but I'm including them all in the enum

# text are enums 1-4
# numeric 5-8
# link 9,10
# image 11-13

  type		enum("unknown", "text/plain", "text/string", "text/html", "text/xml",
		"numeric/integer", "numeric/float", "numeric/double", "numeric/boolean",
		"link/url", "link/image",
		"image/png", "image/jpeg", "image/gif") not null,
  value		blob,

  index (trial_id),
  index (experiment_id)
);

