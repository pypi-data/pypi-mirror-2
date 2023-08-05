# $Id: rowaccess.py,v 1.2 2010/03/17 18:50:06 jribbens Exp $

import jon.wt as wt

class RowAccess(wt.TemplateCode):
  rowaccess_attrib = "row"

  def __getattr__(self, name):
    try:
      return getattr(self, self.rowaccess_attrib)[name]
    except KeyError:
      raise AttributeError(name)
