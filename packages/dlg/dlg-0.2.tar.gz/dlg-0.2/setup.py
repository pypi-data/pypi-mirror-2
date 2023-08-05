#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
import dlg

setup(name='dlg',
    version=dlg.__version__,
    description='python wrapper for dialog/Xdialog/gdialog programs',
    long_description="""goals are to support all dialog features; be compact and easy to use; support whiptail, Xdialog, kdialog, zenity and others in future versions""",
    author=dlg.__author__,
    author_email=dlg.__author_email__,
    url=dlg.__url__,
    download_url=dlg.__download_url__,
    #packages=['dlg',],
    py_modules=['dlg',],
     )

