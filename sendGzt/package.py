# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe  
  
options = {"py2exe":  
            {   "compressed": 1,     
                "optimize": 2,      
                "bundle_files": 1
            }     
          }     
setup(        
    version = "1.2.0",
    description = "工资条邮件发送程序",
    name = "sendMail",
    options = options,
    zipfile = None,
    console = [{"script": "app.py"}],
    )