##
## This makefile provides a convenient mechanism for running the Acro
## tests.
##

all: unit-tests tutorial-tests

tutorial-tests:
	@echo "-------------------------------------------------------------"
	@echo "-------------------------------------------------------------"
	@echo " Acro Tutorials"
	@echo "-------------------------------------------------------------"
	@echo "-------------------------------------------------------------"
	@echo ""
	- @(cd ../../tutorial/acro;\
	for i in `ls *.py` ; do\
	  echo "FILE $$i";\
	  python -t $$i > tmp;\
      dos2unix tmp > /dev/null 2>&1;\
	  output=`diff $${i%.py}.out tmp`;\
	  if [ "$$output" != "" ]; then\
	     echo "  FAIL";\
	  else\
	     echo "  OK";\
	  fi;\
	echo "";\
	done )
	@rm -f ../tutorial/tmp
	@echo ""

unit-tests:
	@echo "-------------------------------------------------------------"
	@echo "-------------------------------------------------------------"
	@echo " Acro Unit Tests"
	@echo "-------------------------------------------------------------"
	@echo "-------------------------------------------------------------"
	@echo ""
	@(cd unit;\
	for i in `ls *.py` ; do echo "FILE $$i"; python -t $$i ; echo ""; done )
	@echo ""
