#
# RNAspace: non-coding RNA annotation platform
# Copyright (C) 2009  CNRS, INRA, INRIA, Univ. Paris-Sud 11
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import smtplib
import urlparse
import logging

from data_manager import data_manager
from trace.event import error_event

class email_sender:

    def __init__(self):
        self.dm = data_manager()
        self.smtpserver = self.dm.get_smtpserver()
        self.port = self.dm.get_smtpserver_port()
        self.login = self.dm.get_smtpserver_login()
        self.password = self.dm.get_smtpserver_password()
        self.from_email = self.dm.get_smtp_from_email()
        self.admin_email = self.dm.get_admin_email()
        self.logger = logging.getLogger("rnaspace")

    def __get_smtp(self):

        if self.port is None:            
            srv = smtplib.SMTP_SSL(self.smtpserver)
        else:
            srv = smtplib.SMTP_SSL(self.smtpserver, int(self.port))

        srv.ehlo()

        if self.login is not None and self.password is not None:
            srv.login(self.login, self.password)            
        return srv

    
    def __send_a_mail(self, from_email, to_emails, msg):
        try:
            srv = self.__get_smtp()
            srv.sendmail(from_email, to_emails, msg)
            srv.quit()
                
        except smtplib.SMTPServerDisconnected:
            e = error_event("-","-","-","Email can not be send: server disconnected. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPConnectError:
            e = error_event("-","-","-","Email can not be send: connect error. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPHeloError:
            e = error_event("-","-","-","Email can not be send: Helo error. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPAuthenticationError:
            e = error_event("-","-","-","Email can not be send: Authentication error. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPRecipientsRefused:
            e = error_event("-","-","-","Email can not be send: all recipients were refused. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPSenderRefused:
            e = error_event("-","-","-","Email can not be send: from_email not valid. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPDataError:
            e = error_event("-","-","-","Email can not be send: data error. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except smtplib.SMTPException:
            e = error_event("-","-","-","Email can not be send: SMTP error. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())

        except:
            e = error_event("-","-","-","Email can not be send. Please check rnaspace.cfg file", 0)
            self.logger.error(e.get_display())


    def send_user_email(self, user_id, project_id, run_id, email, url):
        """
        Send an email to the user with a link to the explore page

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the run id
        email(string)          the email address of the connected user
        url(string)            the url of the running server
        """
        subject = "[RNAspace] Results for job %s" % (project_id)
        authkey = self.dm.get_authkey(user_id, project_id)
        res_url = urlparse.urljoin(url, "explore?authkey=%s" % (authkey))
        ptrace = self.dm.get_project_trace(user_id, project_id)
        predict_events = ptrace.get_predict_events_for_display()
        project_expiration = self.dm.get_project_expiration_days()

        prnas = {}
        nb_rnas = 0
        for evt in predict_events:
            if evt.run_id == run_id:
                nb_rnas += int(evt.nb_prediction)
                try:
                    prnas[evt.gene_finder_name] += int(evt.nb_prediction)
                except:
                    prnas[evt.gene_finder_name] = int(evt.nb_prediction)
        
        body = """\
Dear RNAspace user,

%s rnas have been found in your run %s (job %s):
""" % (str(nb_rnas), run_id, project_id)

        for prna in prnas:
            line = "   - " + prna + " found " + str(prnas[prna]) + " rna(s)" 
            body += """\
%s
""" % (line)

        if int(project_expiration) != 0:
            body += """\

Results are available for %s days at %s.
""" % (project_expiration, res_url)
        else:
            body += """\
Results are available at %s.
""" % (res_url)

        body += """\
From this page, you can explore results of gene finders and perform several 
actions on them (merging, editing, aligning, exporting and so on ...). 

Thanks for using RNAspace !
The RNAspace team
"""
        
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s""" % (self.from_email,
                                                         email,
                                                         subject,
                                                         body)
        self.__send_a_mail(self.from_email, email, msg)


    def send_user_failed_email(self, user_id, project_id, run_id,
                               failed_soft, email, url):
        """
        Send an email to the user to alert him that his job failed

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the run id
        failed_soft({})        list of failed soft
        email(string)          the email address of the connected user
        url(string)            the url of the running server
        """
        subject = "[RNAspace] Results for job %s" % (project_id)
        authkey = self.dm.get_authkey(user_id, project_id)
        res_url = urlparse.urljoin(url, "explore?authkey=%s" % (authkey))
        ptrace = self.dm.get_project_trace(user_id, project_id)
        predict_events = ptrace.get_predict_events_for_display()
        project_expiration = self.dm.get_project_expiration_days()
        
        body = """\
Dear RNAspace user,

An error occured in your run %s on the following predictor(s):
""" % (run_id)
        for (soft, err) in failed_soft:
            line = "   - " + soft + ":" + err
            body += """\
%s
""" % (line)
        body += """\
Please be advised an email has been sent to notify the administrator.
"""
        prnas = {}
        nb_rnas = 0
        for evt in predict_events:
            if evt.run_id == run_id:
                nb_rnas += int(evt.nb_prediction)
                try:
                    prnas[evt.gene_finder_name] += int(evt.nb_prediction)
                except:
                    prnas[evt.gene_finder_name] = int(evt.nb_prediction)
        
        body += """\

%s rnas have been found in this run %s (job %s):
""" % (str(nb_rnas), run_id, project_id)

        for prna in prnas:
            line = "   - " + prna + " found " + str(prnas[prna]) + " rna(s)" 
            body += """\
%s
""" % (line)

        if int(project_expiration) != 0:
            body += """\

Results are available for %s days at %s.
""" % (project_expiration, res_url)
        else:
            body += """\
Results are available at %s.
""" % (res_url)

        body += """\
From this page, you can explore results of gene finders and perform several 
actions on them (merging, editing, aligning, exporting and so on ...). 

Thanks for using RNAspace !
The RNAspace team
"""
        
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s""" % (self.from_email,
                                                         email,
                                                         subject,
                                                         body)
        self.__send_a_mail(self.from_email, email, msg)


    def send_admin_failed_email(self, user_id, project_id, run_id, failed_soft,
                                cmd):
        """
        Send an email to the user with a link to the explore page

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        failed_soft(string)    name of the failed soft
        cmd                    the failed command
        """
        subject = "[RNAspace] RNAspace error"
        
        
        body = """\
Dear RNAspace administrator,

An error occured in RNAspace execution. 
Here are some informations:
   - User: %s
   - Project: %s
   - Run: %s
   - Software: %s
   - Command: %s
   
Please, correct this bug ...

""" % (user_id, project_id, run_id, failed_soft, cmd)
        
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s""" % (self.from_email,
                                                         self.admin_email,
                                                         subject,
                                                         body)
        self.__send_a_mail(self.from_email, [self.admin_email], msg)


    def send_admin_tb(self, tb):
        """
        Send an email to the admin
        """
        subject = "[RNAspace] RNAspace error"
        
        
        body = """\
Dear RNAspace administrator,

An error occured in RNAspace execution. 
Here is the traceback :
%s

Please, correct this bug ...

""" % (tb)
        
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s""" % (self.from_email,
                                                         self.admin_email,
                                                         subject,
                                                         body)
        self.__send_a_mail(self.from_email, [self.admin_email], msg)
