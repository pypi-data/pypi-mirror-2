#!/usr/bin/env python
# Copyright (c) 2010 Hong MinHee <http://dahlia.kr/>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
"""Rocketdive is a non-programmer-friendly GUI frontend for Rocket which is
a modern, multi-threaded, comet-friendly WSGI web server. So, of course, it
depends on Rocket. Its GUI is written by Tkinter. Tested on Mac OS X, Linux
and Windows.

You can download executable binaries for Mac OS X (.dmg packaged .app) and
Windows (standalone .exe) from following URL:

http://bitbucket.org/dahlia/rocketdive/downloads

(The name is borrowed from Japanese artist hide's song of the same title, but
there is no relation between both.)

"""

import multiprocessing
import threading
import os.path
import time
import sys
import logging
import Tkinter as tk
import tkFileDialog
import webbrowser
try:
    import rocket
except ImportError:
    import warnings
    warnings.warn("Module 'rocket' is not loaded")

__version__ = "0.3"
__author__ = "Hong, MinHee"
__email__ = "minhee@dahlia.kr"
__license__ = "MIT License"


SERVER_WAIT = -1
SERVER_ERROR_NONE = 0
SERVER_ERROR_IMPORT = 1
SERVER_ERROR_NAME = 2
SERVER_ERROR_TYPE = 3


class Application(tk.Frame):
    """Rocket Dive application."""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="#ffffff")
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Working Path", bg="#ffffff").grid(row=0, column=0)
        self.workingPathEntry = tk.Entry(self, width=25)
        self.workingPathEntry.grid(row=0, column=1)
        self.workingPathButton = tk.Button(self,
                                           text="Select",
                                           command=self.selectWorkingPath)
        self.workingPathButton.grid(row=0, column=2)
        tk.Label(self, text="Module Name", bg="#ffffff").grid(row=1, column=0)
        self.moduleNameEntry = tk.Entry(self, width=25)
        self.moduleNameEntry.grid(row=1, column=1)
        tk.Label(self, text="Application Variable", bg="#ffffff") \
          .grid(row=2, column=0)
        self.applicationVarEntry = tk.Entry(self, width=25)
        self.applicationVarEntry.grid(row=2, column=1)
        tk.Label(self, text="Port Number", bg="#ffffff").grid(row=3, column=0)
        self.portNumberEntry = tk.Entry(self, width=5)
        self.portNumberEntry.insert(0, "8888")
        self.portNumberEntry.grid(row=3, column=1)
        self.operateButton = tk.Button(self, text="Start", command=self.operate)
        self.operateButton.grid(row=4, column=0)

    def selectWorkingPath(self):
        path = tkFileDialog.askdirectory(parent=self.master)
        self.workingPathEntry.delete(0)
        self.workingPathEntry.insert(0, path)

    def operate(self):
        if hasattr(self, "proc"):
            self.operateButton["text"] = u"Loading\u2026"
            self.stopServer()
            self.operateButton["text"] = "Start"
        else:
            self.startServer()

    def startServer(self):
        self.hideError()
        workingPath = self.workingPathEntry.get().strip()
        moduleName = ".".join(n.strip()
                              for n in self.moduleNameEntry.get().split("."))
        applicationVar = self.applicationVarEntry.get().strip()
        portNumber = self.portNumberEntry.get().strip()
        if not workingPath:
            self.showError("Select the working path.")
        elif not os.path.isdir(workingPath):
            self.showError(workingPath + u" doesn't exist.")
        elif not moduleName:
            self.showError("Fill the module name.")
        elif not applicationVar:
            self.showError("Fill the application variable.")
        elif not portNumber:
            self.showError("Set the port number.")
        else:
            try:
                self.portNumber = int(portNumber)
            except ValueError:
                self.showEror("Port number must be an integer.")
            self.operateButton["text"] = u"Loading\u2026"
            try:
                self.proc, self.logConn = run_server(workingPath,
                                                     moduleName,
                                                     applicationVar,
                                                     self.portNumber)
            except ImportError:
                self.showError("Cannot import {0} module".format(moduleName))
            except NameError:
                self.showError("Name {0} is undefined".format(applicationVar))
            else:
                self.startLogging()
                self.operateButton["text"] = "Stop"
                webbrowser.open_new("http://localhost:{0}/".format(portNumber))
                return
        self.operateButton["text"] = "Start"

    def watchLogging(self):
        if hasattr(self, "proc") and hasattr(self, "logConn"):
            if self.logConn.poll():
                record = self.logConn.recv()
                if record:
                    self.loggingText.insert(tk.END, record.getMessage())
                    self.loggingText.insert(tk.END, "\n")
                    self.loggingText.yview(tk.MOVETO, 1.0)
            self.loggingThread = self.loggingText.after(100, self.watchLogging)

    def startLogging(self):
        self.loggingText = tk.Text(self, bg="#000", fg="#fff")
        self.loggingText.grid(row=5, column=0, columnspan=3)
        self.watchLogging()

    def stopServer(self):
        if hasattr(self, "proc"):
            self.proc.terminate()
            self.proc.join()
            del self.proc
            del self.logConn
            loggingText = self.loggingText
            loggingText.destroy()
            del self.loggingText
            self.after_cancel(self.loggingThread)
            del self.loggingThread

    def showError(self, message):
        if not hasattr(self, "errorMessageLabel"):
            self.errorMessageLabel = tk.Label(self, bg="#ffffff", fg="red")
            self.errorMessageLabel.grid(row=4, column=1)
        self.errorMessageLabel["text"] = message

    def hideError(self):
        if hasattr(self, "errorMessageLabel"):
            self.errorMessageLabel["text"] = ""


class LoggingHandler(logging.Handler):

    def __init__(self, connection, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.connection = connection

    def emit(self, record):
        self.connection.send(record)

    def close(self):
        self.connection.close()


def run_server(working_path, module_name, application_var, port):
    error = multiprocessing.Value("i", SERVER_WAIT)
    parent_conn, child_conn = multiprocessing.Pipe()
    args = working_path, module_name, application_var, port, child_conn, error
    proc = multiprocessing.Process(target=server, args=args)
    proc.start()
    while error.value == SERVER_WAIT:
        time.sleep(0.1)
    if error.value == SERVER_ERROR_IMPORT:
        raise ImportError("No module named " + module_name)
    elif error.value == SERVER_ERROR_NAME:
        raise NameError("name {0!r} is not defined".format(application_var))
    elif error.value == SERVER_ERROR_TYPE:
        raise TypeError("name {0!r} is not callable".format(application_var))
    return proc, parent_conn


def server(working_path, module_name, application_var, port,
           logging_connection, error):
    if os.path.isdir(working_path):
        sys.path.insert(0, working_path)
    try:
        mod = __import__(module_name)
    except ImportError:
        error.value = SERVER_ERROR_IMPORT
        return
    submodules = module_name.split(".")
    for submodule in submodules[1:]:
        if not hasattr(mod, submodule):
            error.value = SERVER_ERROR_IMPORT
            return
        mod = getattr(mod, submodule)
    if not hasattr(mod, application_var):
        error.value = SERVER_ERROR_NAME
        return
    application = getattr(mod, application_var)
    if not callable(application):
        error.value = SERVER_ERROR_TYPE
        return
    error.value = SERVER_ERROR_NONE
    log = logging.getLogger("Rocket")
    log.setLevel(logging.INFO)
    log.addHandler(LoggingHandler(logging_connection))
    httpd = rocket.Rocket(("0.0.0.0", int(port)),
                          "wsgi", {"wsgi_app": application})
    httpd.start()


def main():
    root = tk.Tk()
    root.title("ROCKET DIVE")
    application = Application(master=root)
    application.mainloop()
    application.stopServer()
    try:
        root.destroy()
    except tk.TclError:
        pass


if __name__ == "__main__":
    main()

