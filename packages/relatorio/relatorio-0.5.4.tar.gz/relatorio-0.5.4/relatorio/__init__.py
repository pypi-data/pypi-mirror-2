"""
relatorio
=========

A templating library which provides a way to easily output all kind of
different files (odt, ods, png, svg, ...). Adding support for more filetype is
easy: you just have to create a plugin for this.

relatorio also provides a report repository allowing you to link python objects
and report together, find reports by mimetypes/name/python objects.
"""
from relatorio.reporting import MIMETemplateLoader, ReportRepository, Report
import templates

__version__ = '0.5.4'
