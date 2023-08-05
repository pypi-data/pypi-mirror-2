import codecs
import xmlrpclib
import os
import logging
from string import Template

from assignmenttree import AssignmentSync, Info, overwriteable_filename, \
    overwrite
from cli import Command, log_fault, format_long_message


log = logging.getLogger('devilry')


class ExaminerCommand(Command):
    """ Base class for all examiner commands. """
    urlpath = '/xmlrpc_examiner/'


class ListAssignments(ExaminerCommand):
    name = 'list'
    short_info = 'List assignments where the authenticated user is examiner.'

    def command(self):
        self.read_config()
        server = self.get_serverproxy()
        try:
            assignments = server.list_active_assignments()
        except xmlrpclib.Fault, e:
            log_fault(e)
        else:
            log.info('Active assignments:')
            for assignment in assignments:
                log.info('* %(path)s' % assignment)


class ListAssignmentGroups(ExaminerCommand):
    name = 'list-groups'
    short_info = 'List assignment groups on a given assignment.'
    args_help = '<assignment-path>'

    def command(self):
        self.validate_argslen(1)
        self.read_config()
        server = self.get_serverproxy()
        assignmentpath = self.args[0]
        try:
            groups = server.list_assignmentgroups(assignmentpath)
        except xmlrpclib.Fault, e:
            log_fault(e)
        else:
            log.info('%16s  %s' % ('ID', 'STUDENT(S)'))
            for group in groups:
                groupinfo = "%15d)  %-45s (deliveries: %d)" % (
                    group['id'],
                    ', '.join(group['students']),
                    group['number_of_deliveries'])
                log.info(groupinfo)


class Sync(ExaminerCommand):
    name = 'sync'
    short_info = 'Sync all deliveries (including all files) where the '\
            'authenticated user is examiner.'
    description = """
File hierarchy
==============

[assignment path]
    [assignment group members (usernames separated with -)]
        [deliveries numbered from 1 and up, 1 beeing the first delivery]
            feedback.rst
            files/
                [all files in the delivery]


Overwriting files
=================

The sync command does not overwrite any files except the ones it is supposed
to overwrite. Those files have their name prefixed with ".overwriteable-".
If you want "sync" to overwrite other files, you have to delete them
yourself, and re-run sync.

Some files have to be overwritten, but are backed up if needed. Backup is
needed if the file has local modifications.

The backup is just the filename suffixed with ".bak-N", where N is the
smallest unused number which is greater than 0. You will meet this behavior
with "feedback.rst", and with a plug-in specific file if the assignment uses
a grade plug-in which requires you to edit a file instead of using the "-g"
option with the feedback command.
"""

    def command(self):
        self.read_config()
        try:
            AssignmentSync(self.find_rootdir(), self.get_cookiepath(),
                    self.get_serverproxy(), self.get_url(),
                    self.get_auth_cookiepath())
        except xmlrpclib.Fault, e:
            log_fault(e)



class FeedbackCmdBase(ExaminerCommand):
    """ Base class for Feedback and PublishFeedback. """

    def direrror(self):
        if len(self.args) > 0:
            log.error('The given directory is not a delivery-directory.')
        else:
            log.error('You are not in a delivery-directory.')
        raise SystemExit()

    def _get_info(self, deliverydir):
        try:
            return Info.read_open(deliverydir, 'Delivery')
        except Info.FileWrongTypeError, e:
            self.direrror()
        except Info.FileDoesNotExistError, e:
            self.direrror()

    def _get_deliverydir(self):
        if len(self.args) > 0:
            deliverydir = os.path.abspath(os.path.normpath(self.args[0]))
        else:
            deliverydir = os.path.abspath(os.getcwd())
        return deliverydir

    def _refresh_info(self, server, deliveryinfo):
        feedback = server.get_feedback(deliveryinfo.get_id())
        AssignmentSync.set_feedbackinfo(deliveryinfo.get_dirpath(),
                feedback)


class Feedback(FeedbackCmdBase):
    name = 'feedback'
    short_info = 'Submit feedback on a delivery.'

    def add_options(self):
        self.op.add_option("-t", "--feedback-text", metavar="TEXT",
            dest="text", default='', help='Feedback text.')
        self.op.add_option("-g", "--grade", metavar="GRADE",
            dest="grade", default=None, help='Grade.')
        self.op.add_option("-f", "--feedback-format",
            metavar="rst|txt", dest="format",
            default='rst', help='Feedback format.')

    def _get_feedback_text(self, deliverydir):
        """ Get feedback text from arguments or file. """
        feedbackfile = os.path.join(deliverydir, 'feedback.rst')
        if self.opt.text:
            log.debug('Feedback found in commandline argument -t.')
            text = self.opt.text
        else:
            log.debug('Feedback not found in commandline argument -t. ' \
                    'Trying file feedback.rst.')
            if os.path.isfile(feedbackfile):
                log.info('Found feedback in file feedback.rst.')
                try:
                    text = codecs.open(feedbackfile, 'r', 'utf-8').read()
                except ValueError, e:
                    log.error('Could not read feedback.rst using as '\
                            'utf-8 text. You should use utf-8 encoding '\
                            'on feedback.rst.')
                    raise SystemExit()
                else:
                    text = text.encode('utf-8')
            else:
                log.debug('Feedback not found in commandline argument -t or ' \
                        'in file feedback.rst. Feedback text is empty.')
                text = None
        if text:
            log.info('Feedback format: %s.' % self.opt.format)
        return text, feedbackfile

    def _get_assignmentinfo(self, deliverydir):
        groupdir = os.path.dirname(deliverydir)
        assignmentdir = os.path.dirname(groupdir)
        return Info.read_open(assignmentdir, 'Assignment')

    def _get_grade(self, assignmentinfo):
        gradeconf_filename = assignmentinfo.get('gradeconf_filename')
        if gradeconf_filename:
            #gradeconf_help = assignmentinfo.get('gradeconf_help')
            grade = open(gradeconf_filename, 'rb').read()
        else:
            grade = self.opt.grade
            if not grade:
                log.error('A grade is required. See --help for more info.')
                raise SystemExit()
        return grade

    def command(self):
        self.read_config()
        deliverydir = self._get_deliverydir()
        info = self._get_info(deliverydir)
        assignmentinfo = self._get_assignmentinfo(deliverydir)
        grade = self._get_grade(assignmentinfo)
        text, feedbackfile = self._get_feedback_text(deliverydir)

        server = self.get_serverproxy()
        try:
            ok_message = server.set_feedback(info.get_id(), text,
                    self.opt.format, grade)
        except xmlrpclib.Fault, e:
            log.error(format_long_message('ERROR MESSAGE', e.faultString,
                False))
            log.error('Setting feedback failed. See error-message above.')
        else:
            lastsave_filename = overwriteable_filename('feedback.lastsave.rst')
            overwrite(deliverydir, lastsave_filename, text)
            open(feedbackfile, 'wb').write(text)
            if ok_message:
                log.info(format_long_message('FEEDBACK SUCCESSFULLY SAVED',
                    ok_message))
            else:
                log.info('Feedback successfully saved.')
            self._refresh_info(server, info)
            info = self._get_info(deliverydir)
            if info.get('feedback_published') == "False":
                log.info('')
                log.info('The feedback you saved was not published and is '\
                        'therefore not visible to the student. Use: ')
                log.info('   devilry-examiner.py publish')
                log.info('to publish the feedback.')


class PublishFeedback(FeedbackCmdBase):
    name = 'publish'
    short_info = 'Publish a feedback.'
    publish = True

    def command(self):
        self.read_config()
        deliverydir = self._get_deliverydir()
        info = self._get_info(deliverydir)
        server = self.get_serverproxy()
        try:
            ok_message = server.set_feedback_published(info.get_id(),
                    self.publish)
        except xmlrpclib.Fault, e:
            log_fault(e)
        else:
            if self.publish:
                log.info('Feedback successfully published.')
            else:
                log.info('Feedback unpublished.')
            self._refresh_info(server, info)

class UnpublishFeedback(PublishFeedback):
    name = 'unpublish'
    short_info = 'Un-publish a feedback.'
    publish = False


class InfoCmd(Command):
    name = 'info'
    short_info = 'Show info about current directory.'
    args_help = ''

    def _assignment(self, info):
        print 'Type: %s' % info.get('type')
        print 'Id: %s' % info.get('id')
        print 'Long name: %s' % info.get('long_name')
        print 'Publishing time: %s' % info.get('publishing_time')

    def _assignmentgroup(self, info):
        print 'Type: %s' % info.get('type')
        print 'Id: %s' % info.get('id')
        print 'Name: %s' % (info.get('name') or '#Not defined#')
        print 'Deliveries:'
        numbers = [n for n in os.listdir(info.get_dirpath()) if n.isdigit()]
        numbers.sort()
        numbers.reverse()
        for num in numbers:
            deliveryinfo = Info.read_open(os.path.join(info.get_dirpath(),
                num))
            print "   %(number)s) %(time_of_delivery)s" % deliveryinfo

    def _delivery(self, info):
        print 'Type: %(type)s' % info
        print 'Id: %(id)s' % info
        print 'Number: %(number)s' % info
        if info.get('feedback_text'):
            print 'Feedback published: %(feedback_published)s' % info
            print 'Feedback last modified: %(feedback_last_modified)s' % info
            print 'Feedback last modified by: %(feedback_last_modified_by)s' % info
            print 'Current feedback format: %(feedback_format)s' % info
            print 'Current feedback text:'
            print info['feedback_text']

    def command(self):
        directory = os.getcwd()
        try:
            info = Info.read_open(directory)
        except Info.FileDoesNotExistError, e:
            log.error('Not in a directory containing a info-file.')
            raise SystemExit()
        typename = info.get('type')
        if typename == 'Assignment':
            self._assignment(info)
        elif typename == 'AssignmentGroup':
            self._assignmentgroup(info)
        elif typename == 'Delivery':
            self._delivery(info)
        else:
            log.error('Invalid type: %s.' % typename)
            raise SystemExit()



class Guide(Command):
    name = 'guide'
    short_info = 'Show a tutorial/howto.'
    def command(self):
        guide = """To get started, initialize a devilry-checkout with these
steps:
    1. Create a new directory (we will call this the checkout-directory) and
       change to it.
        
        ~$ mkdir ~/devilrycheckout
        ~$ cd ~/devilrycheckout

    2. Initialize with the devilry-server:

        ~devilrycheckout/$ $prog init <server-url>

       Where server-url is the url to the root of the devilry-site you wish
       to initialize with. This might be something like
       "http://example.com/", or "http://example.com/devilry/". You can
       check if the url is correct by suffixing it with "/xmlrpc/" and open
       it in a browser. If the url takes you to the xmlrpc documentation,
       you have the correct url.

    3. Login using:

        ~devilrycheckout/$ $prog login

        If your username in the current shell session is not the same as your
        username with the devilry server, you must use:

        ~devilrycheckout/$ $prog login -u myuser

    4. Sync every delivery on every active assignment using:

        ~devilrycheckout/$ $prog sync

    5. See the help for 'sync', 'info' and 'feedback' for more information:

        ~devilrycheckout/$ $prog help sync
        ~devilrycheckout/$ $prog help info
        ~devilrycheckout/$ $prog help feedback

When you wish to update the local sync with new deliveries, or feedback
submitted by other examiners (if you work on assignments with more than one
examiner on each group), just repeat steps 3 and 4 within any directory
below the checkout-directory. You might not have to login more than about
once a day, but this varies depending on how the devilry-server is
configured.
"""
        print Template(guide).safe_substitute(prog=self.prog)
