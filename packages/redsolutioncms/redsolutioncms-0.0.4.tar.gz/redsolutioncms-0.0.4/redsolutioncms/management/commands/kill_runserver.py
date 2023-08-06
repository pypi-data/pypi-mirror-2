# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from redsolutioncms.models import ProcessTask
import time
import os, signal, sys

class Command(BaseCommand):

    def handle(self, *args, **options):
        runserver_tasks = ProcessTask.objects.filter(process_finished=False,
            task__contains=' runserver', executed=True)
        for task in runserver_tasks:
            if task.pid:
                if os.sys.platform == 'win32':
                        import ctypes
                        CTRL_BREAK_EVENT = 1
                        GenerateConsoleCtrlEvent = ctypes.windll.kernel32.GenerateConsoleCtrlEvent
                        GenerateConsoleCtrlEvent(CTRL_BREAK_EVENT, task.pid)
                else:
                    try:
                        os.kill(task.pid, signal.SIG_DFL)
                    except OSError:
                        pass
                    else:
                        sys.stdout.flush()
                        os.killpg(os.getpgid(task.pid), signal.SIGINT)
                task.process_finished = True
                task.save()
