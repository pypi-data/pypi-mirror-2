"""
A Trial IReporter plugin that gathers coverage.py code-coverage information.

Once this plugin is installed, trial can be invoked a new --reporter option:

  trial --reporter-bwverbose-coverage ARGS

Once such a test run has finished, there will be a .coverage file in the
top-level directory. This file can be turned into a directory of .html files
(with index.html as the starting point) by running:

 coverage html -d OUTPUTDIR --omit=PREFIX1,PREFIX2,..

The 'coverage' tool thinks in terms of absolute filenames. 'coverage' doesn't
record data for files that come with Python, but it does record data for all
the various site-package directories. To show only information for your
source code files, you should provide --omit prefixes for everything else.
This probably means something like:

  --omit=/System/,/Library/,/usr/

Before using this, you need to install the 'coverage' package, which will
provide an executable tool named 'coverage' ('python-coverage' on Ubuntu) as
well as an importable library. 'coverage report' will produce a basic text
summary of the coverage data.
"""

import os, shutil

from pyutil import fileutil

import twisted.trial.reporter

import setuptools

# These plugins are registered via twisted/plugins/trialcoveragereporterplugin.py .
# See the notes there for an explanation of how that works.

# Some notes about how trial Reporters are used:
# * Reporters don't really get told about the suite starting and stopping.
# * The Reporter class is imported before the test classes are.
# * The test classes are imported before the Reporter is created. To get
#   control earlier than that requires modifying twisted/scripts/trial.py
# * Then Reporter.__init__ is called.
# * Then tests run, calling things like write() and addSuccess(). Each test is
#   framed by a startTest/stopTest call.
# * Then the results are emitted, calling things like printErrors,
#   printSummary, and wasSuccessful.
# So for code-coverage (not including import), start in __init__ and finish
# in printSummary. To include import, we have to start in our own import and
# finish in printSummary.

# We keep our notes about previous best code-coverage results in a
# folder named ".coverage-results".
RES_DIRNAME='.coverage-results'
fileutil.make_dirs(RES_DIRNAME)
BEST_DIRNAME=os.path.join(RES_DIRNAME, 'best')
fileutil.make_dirs(BEST_DIRNAME)
BEST_COVERAGE_FNAME=os.path.join(BEST_DIRNAME, '.coverage')
SUMMARY_FNAME=os.path.join(RES_DIRNAME, 'summary.txt')
BEST_SUMMARY_FNAME=os.path.join(BEST_DIRNAME, 'summary.txt')
VERSION_STAMP_FNAME=os.path.join(RES_DIRNAME, 'version-stamp.txt')
BEST_VERSION_STAMP_FNAME=os.path.join(BEST_DIRNAME, 'version-stamp.txt')

import coverage
import pkg_resources

from coverage.report import Reporter as CoverageReporter
from coverage.summary import SummaryReporter as CoverageSummaryReporter
import coverage.summary
from coverage.results import Numbers

def import_all_python_files(packages):
    for package in packages:
        packagedir = '/'.join(package.split('.'))

        for (dirpath, dirnames, filenames) in os.walk(packagedir):
            for filename in (filename for filename in filenames if filename.endswith('.py')):
                dirs = dirpath.split("/")
                if filename != "__init__.py":
                    dirs.append(filename[:-3])
                import_str = "%s" % ".".join(dirs)
                if import_str not in ("setup", __name__):
                    try:
                        __import__(import_str)
                    except ImportError, le:
                        if 'No module named' in str(le):
                            # Oh whoops I guess that Python file we found isn't a module of this package. Nevermind.
                            pass
                        raise

packages = setuptools.find_packages('.')
cov = coverage.coverage(require_prefixes=packages, branch=True, auto_data=True)
cov.start()
import_all_python_files(packages)
cov.stop()
cov.save()

import errno
def move_if_present(src, dst):
    try:
        shutil.move(src, dst)
    except EnvironmentError, le:
        # Ignore "No such file or directory", re-raise any other exception.
        if (le.args[0] != 2 and le.args[0] != 3) or (le.args[0] != errno.ENOENT):
            raise

def copy_if_present(src, dst):
    try:
        shutil.copy2(src, dst)
    except EnvironmentError, le:
        # Ignore "No such file or directory", re-raise any other exception.
        if (le.args[0] != 2 and le.args[0] != 3) or (le.args[0] != errno.ENOENT):
            raise

def parse_out_unc_and_part(summarytxt):
    for line in summarytxt.split('\n'):
        if line.startswith('Name'):
            linesplit = line.split()
            missix = linesplit.index('Miss')
            try:
                brpartix = linesplit.index('BrPart')
            except ValueError, le:
                print "ERROR, this tool requires a version of coverage.py new enough to report branch coverage, which was introduced in coverage.py v3.2."
                le.args = tuple(le.args + (linesplit,))
                raise

        if line.startswith('TOTAL'):
            linesplit = line.split()
            return (int(linesplit[missix]), int(linesplit[brpartix]))
    raise Exception("Control shouldn't have reached here because there should have been a line that started with 'TOTAL'. The full summary text was %r." % (summarytxt,))

class ProgressionReporter(CoverageReporter):
    """A reporter for testing whether your coverage is improving or degrading. """

    def __init__(self, coverage, show_missing=False, ignore_errors=False):
        super(ProgressionReporter, self).__init__(coverage, ignore_errors)
        self.summary_reporter = CoverageSummaryReporter(coverage, show_missing=show_missing, ignore_errors=ignore_errors)

    def coverage_progressed(self):
        """ Returns 0 if coverage has regressed, 1 if there was no
        existing best-coverage summary, 2 if coverage is the same as
        the existing best-coverage summary, 3 if coverage is improved
        compared to the existing best-coverage summary. """
        if not hasattr(self, 'bestunc'):
            return 1

        if (self.curtot == self.besttot) and (self.curunc == self.bestunc):
            return 2

        if (self.curtot <= self.besttot) and (self.curunc <= self.bestunc):
            return 3
        else:
            return 0

    def report(self, morfs, omit_prefixes=None, outfile=None):
        """Writes a report summarizing progression/regression."""
        # First we use our summary_reporter to generate a text summary of the current version.
        if outfile is None:
            outfile = SUMMARY_FNAME
        outfileobj = open(outfile, "w")
        self.summary_reporter.report(morfs, omit_prefixes=omit_prefixes, outfile=outfileobj)
        outfileobj.close()

        self.curunc, self.curpart = parse_out_unc_and_part(fileutil.read_file(SUMMARY_FNAME, mode='rU'))
        self.curtot = self.curunc + self.curpart

        # Then we see if there is a previous best version and if so what its count of uncovered and partially covered lines was.
        try:
            bestsum = fileutil.read_file(BEST_SUMMARY_FNAME, mode='rU')
        except IOError:
            pass
        else:
            self.bestunc, self.bestpart = parse_out_unc_and_part(bestsum)
            self.besttot = (self.bestunc + self.bestpart)

        progression = self.coverage_progressed()
        if progression == 0:
            print "WARNING code coverage regression"
            print "Previous best coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.besttot, self.bestunc, self.bestpart)
            print "Current coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.curtot, self.curunc, self.curpart)
            return progression

        if progression == 1:
            print "code coverage summary"
            print "There was no previous best code-coverage summary found."
            print "Current coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.curtot, self.curunc, self.curpart)
        elif progression == 2:
            print "code coverage totals unchanged"
            print "Previous best coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.besttot, self.bestunc, self.bestpart)
            print "Current coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.curtot, self.curunc, self.curpart)
        elif progression == 3:
            print "code coverage improvement!"
            print "Previous best coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.besttot, self.bestunc, self.bestpart)
            print "Current coverage left %d total lines untested (%d lines uncovered and %d lines partially covered)." % (self.curtot, self.curunc, self.curpart)

        shutil.copy2('.coverage', BEST_COVERAGE_FNAME)
        shutil.copy2(SUMMARY_FNAME, BEST_SUMMARY_FNAME)
        copy_if_present(VERSION_STAMP_FNAME, BEST_VERSION_STAMP_FNAME)
        return progression

class CoverageTextReporter(twisted.trial.reporter.VerboseTextReporter):
    def __init__(self, *args, **kwargs):
        twisted.trial.reporter.VerboseTextReporter.__init__(self, *args, **kwargs)
        self.pr = None

    def startTest(self, test):
        res = twisted.trial.reporter.VerboseTextReporter.startTest(self, test)
        cov.start()
        # print "%s.startTest(%s) self.collector._collectors: %s" % (self, test, cov.collector._collectors)
        return res

    def stopTest(self, test):
        res = twisted.trial.reporter.VerboseTextReporter.stopTest(self, test)
        # print "%s.stopTest(%s) self.collector._collectors: %s" % (self, test, cov.collector._collectors)
        cov.stop()
        cov.save()
        return res

    def stop_coverage(self):
        print "Coverage results written to %s" % ('.coverage',)
        assert self.pr is None, self.pr
        self.pr = ProgressionReporter(cov)
        self.pr.report(None, omit_prefixes=os.environ.get('COVERAGE_OMITS', ''))
    def printSummary(self):
        # for twisted-2.5.x
        self.stop_coverage()
        return twisted.trial.reporter.VerboseTextReporter.printSummary(self)
    def done(self):
        # for twisted-8.x
        self.stop_coverage()
        return twisted.trial.reporter.VerboseTextReporter.done(self)

    def wasSuccessful(self):
        return super(CoverageTextReporter, self).wasSuccessful() and self.pr.coverage_progressed()
