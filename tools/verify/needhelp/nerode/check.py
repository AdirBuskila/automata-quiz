# -*- coding: utf-8 -*-
"""Machine check of the nerode guided course: python tools/verify/needhelp/nerode/check.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common

if __name__ == "__main__":
    common.run("nerode")
