#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
الملف الرئيسي لتشغيل التطبيق.
"""

from views.main_win import MainWin

if __name__ == '__main__':
    app = MainWin()
    app.mainloop()
