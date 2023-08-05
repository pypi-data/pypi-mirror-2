#!/usr/bin/env python

from distutils.core import setup, Extension

setup (name = "pykf",
       version = "0.3.5",
       description = "Japanese Kanji code filter",
       author = "Atsuo Ishimoto",
       author_email = "ishimoto@gembook.org",
       url = "http://sourceforge.jp/projects/pykf/",
       classifiers = [
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"],
     license="MIT License",
     ext_modules = [
           Extension("pykf",
                     [
                        "src/pykf.c",
                        "src/converter.c",
                        "src/jis0213.c",
                        "src/mskanji.c",
                      ])])
