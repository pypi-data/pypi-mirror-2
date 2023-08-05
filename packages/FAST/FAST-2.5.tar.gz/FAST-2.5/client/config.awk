#
# AWK script to parse uncommented environment variables out of
# the file it is called to process.  It then dumps a batch
# script to stdout that sets those variables using CSH syntax.
# Original version of this script was an inline argument to
# gawk in cron_script.
#
# Last condition in last if-statement simplified by using AWK
# regexp syntax instead of substring parsing (seek beginning
# of line followed by #).  Notice also that the # in that
# condition is escaped to avoid causing AWK to comment out the
# closing parentheses.
#
BEGIN {state=1}
{
  if ($1 == "Test")
    state=2
  if ((state == 1) && ($1 != "") && ($1 !~ /^\#/))
    print "setenv "$0"\n"
}
