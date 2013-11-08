from __future__ import with_statement

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:58:31 2013

@author: laure.hugo@cea.fr
"""

import os

from soma_workflow.client import Job
from soma_workflow.client import FileTransfer
from soma_workflow.test.workflow_examples import WorkflowExamples


class WorkflowExamplesTransfer(WorkflowExamples):

    def __init__(self):
        '''
        The input and ouput files are temporary files on the computing
        resource and these files can be transfered from and to the
        computing resource using soma workflow API
        '''
        super(WorkflowExamplesTransfer, self).__init__()

        # Initialize the dictionaries
        self.tr_file = {}
        self.tr_script = {}
        self.tr_stdin = {}
        self.lo_stdout = {}
        self.lo_stderr = {}
        self.lo_out_model_file = {}

        complete_path = os.path.join(self.examples_dir, "complete")

        self.tr_file[0] = FileTransfer(True,
                                       os.path.join(complete_path, "file0"),
                                       168, "file0")
        self.tr_in_dir = FileTransfer(True, self.examples_dir, 168, "in_dir")
        self.tr_img_file = FileTransfer(
            True, os.path.join(self.examples_dir,
                               "special_transfers/dir_contents.py"),
            128, "img_file",
            [os.path.join(self.examples_dir, "special_transfers/example.img"),
             os.path.join(self.examples_dir, "special_transfers/example.hdr")])
        self.tr_exceptionJobScript = FileTransfer(
            True, os.path.join(self.examples_dir, "simple/exceptionJob.py"),
            168, "exception_job")
        self.tr_sleep_script = FileTransfer(
            True, os.path.join(self.examples_dir, "simple/sleep_job.py"),
            168, "sleep_job")
        self.tr_cmd_check_script = FileTransfer(
            True, os.path.join(self.examples_dir, "command/argument_check.py"),
            168, "cmd_check")
        self.tr_dir_contents_script = FileTransfer(
            True, os.path.join(self.examples_dir,
                               "special_transfers/dir_contents.py"),
            168, "dir_contents")
        self.tr_mff_script = FileTransfer(
            True, os.path.join(self.examples_dir,
                               "special_transfers/multiple_file_format.py"),
            168, "mdd_script")
        self.tr_out_dir = FileTransfer(
            False, os.path.join(self.output_dir, "transfered_dir"),
            168, "out_dir")
        self.tr_img_out_file = FileTransfer(
            False, os.path.join(self.output_dir, "example.img"),
            168, "img_out",
            [os.path.join(self.output_dir, "example.img"),
             os.path.join(self.output_dir, "example.hdr")])

        self.tr_dir_contents_stdout = os.path.join(
            self.examples_dir,
            "special_transfers/tr_dir_contents_stdout")

        self.lo_stdout1_exception_model = os.path.join(
            self.examples_dir,
            "simple/outputModels/stdout_exception_job")
        self.lo_stderr1_exception_model = os.path.join(
            self.examples_dir,
            "simple/outputModels/stderr_exception_job")
        self.lo_in_dir = self.examples_dir
        self.lo_mff_stdout = os.path.join(
            self.examples_dir,
            'special_transfers/multiple_file_format_stdout')
        self.lo_stdout_command_model = os.path.join(
            self.examples_dir,
            "command/stdout_special_command")

        for i in range(1, 5):
            self.tr_script[i] = FileTransfer(
                True, os.path.join(complete_path, "job" + str(i) + ".py"),
                168, "job" + str(i) + "_py")
            self.tr_stdin[i] = FileTransfer(
                True, os.path.join(complete_path, "stdin" + str(i)),
                168, "stdin" + str(i))
            self.lo_stdout[i] = os.path.join(complete_path,
                                             "outputModels/stdoutjob" + str(i))
            self.lo_stderr[i] = os.path.join(complete_path,
                                             "outputModels/stderrjob" + str(i))

        for i in [11, 12, 2, 3, 4]:
            self.tr_file[i] = FileTransfer(
                False, os.path.join(self.output_dir, "file" + str(i)),
                168, "file" + str(i))
            self.lo_out_model_file[i] = os.path.join(
                complete_path,
                "outputModels/file" + str(i))

    def job1(self, option=None):
        time_to_wait = 2
        job_name = "job1"
        job1 = Job(["python",
                    self.tr_script[1], self.tr_file[0],
                    self.tr_file[11], self.tr_file[12],
                    repr(time_to_wait)],
                   [self.tr_file[0], self.tr_script[1], self.tr_stdin[1]],
                   [self.tr_file[11], self.tr_file[12]],
                   self.tr_stdin[1], False, 168, job_name,
                   native_specification=option)
        return job1

    def job2(self):
        time_to_wait = 2
        job_name = "job2"
        job2 = Job(["python",
                    self.tr_script[2], self.tr_file[11],
                    self.tr_file[0], self.tr_file[2],
                    repr(time_to_wait)],
                   [self.tr_file[0], self.tr_file[11],
                    self.tr_script[2], self.tr_stdin[2]],
                   [self.tr_file[2]],
                   self.tr_stdin[2], False, 168, job_name)
        return job2

    def job3(self):
        time_to_wait = 2
        job_name = "job3"
        job3 = Job(["python",
                    self.tr_script[3], self.tr_file[12],
                    self.tr_file[3], repr(time_to_wait)],
                   [self.tr_file[12], self.tr_script[3], self.tr_stdin[3]],
                   [self.tr_file[3]],
                   self.tr_stdin[3], False, 168, job_name)
        return job3

    def job4(self):
        time_to_wait = 10
        job_name = "job4"
        job4 = Job(["python",
                    self.tr_script[4], self.tr_file[2],
                    self.tr_file[3], self.tr_file[4],
                    repr(time_to_wait)],
                   [self.tr_file[2], self.tr_file[3],
                    self.tr_script[4], self.tr_stdin[4]],
                   [self.tr_file[4]],
                   self.tr_stdin[4], False, 168, job_name)
        return job4

    def job_test_command_1(self):
        test_command = Job(["python",
                            self.tr_cmd_check_script,
                            "[13.5, 14.5, 15.0]", '[13.5, 14.5, 15.0]',
                            "['un', 'deux', 'trois']",
                            '["un", "deux", "trois"]'],
                           [self.tr_cmd_check_script, self.tr_script[1],
                            self.tr_script[2], self.tr_script[3]],
                           [], None, False, 168, "test_command_1")
        return test_command

    def job_test_dir_contents(self):
        job = Job(["python", self.tr_dir_contents_script,
                  self.tr_in_dir, self.tr_out_dir],
                  [self.tr_dir_contents_script, self.tr_in_dir],
                  [self.tr_out_dir],
                  None, False, 168, "dir_contents")
        return job

    def job_test_multi_file_format(self):
        job = Job(["python", self.tr_mff_script,
                   (self.tr_img_file, "example.img"),
                   (self.tr_img_out_file, "example.img")],
                  [self.tr_mff_script, self.tr_img_file],
                  [self.tr_img_out_file],
                  None, False, 168, "multi file format test")
        return job

    def job_sleep(self, period):
        complete_path = os.path.join(self.examples_dir, "complete")
        transfer = FileTransfer(
            True, os.path.join(complete_path, "file0"),
            168, "file0")
        job = Job(["python", self.tr_sleep_script, repr(period)],
                  [self.tr_sleep_script, transfer], [],
                  None, False, 168, "sleep " + repr(period) + " s")
        return job

    def job1_exception(self):
        job = Job(["python", self.tr_exceptionJobScript],
                  [self.tr_exceptionJobScript,
                   self.tr_file[0],
                   self.tr_script[1],
                   self.tr_stdin[1]],
                  [self.tr_file[11], self.tr_file[12]],
                  self.tr_stdin[1], False, 168, "job1 with exception")
        return job

    def job3_exception(self):
        job = Job(["python", self.tr_exceptionJobScript],
                  [self.tr_exceptionJobScript,
                   self.tr_file[12],
                   self.tr_script[3],
                   self.tr_stdin[3]],
                  [self.tr_file[3]],
                  self.tr_stdin[3], False, 168, "job3 with exception")
        return job