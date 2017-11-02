# coding:utf-8

from __future__ import print_function
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django import forms
from .models import CreateRecord
import os
import sys
import locale
import codecs
import traceback
import json

def IndexView(request):
    LogOutput('log/')
    return render(request,'s3log/index.html')

def SimpleCharDet(b_str):
    def TryDecode(b_str, c_code):
        try:
            b_str.decode(c_code)
            return c_code
        except UnicodeDecodeError:
            return 'UDError'
    c_code_list = ['us-ascii', 'utf-8', 'cp932', 'eucjp']
    for c_code in c_code_list:
        if TryDecode(b_str, c_code) != c_code_list: return c_code
    return 'unknown'

def GetCoding(filepath):
    locale.setlocale(locale.LC_ALL, '')
    maxsize = 1 * 1024 * 1024
    def SysExit(e, errorMsg):
        sys.exit("Error: {4} '{0}' [{1}]: {2}".format(filepath, e.errno, e.strerror, errorMsg))
    def TryRead(f_in):
        try:
            return f_in.read(maxsize)
        except IOError as e:
            SysExit(e, 'cannot read from file')
    def TryOpen():
        try:
            with open(filepath, 'rb') as f_in: return TryRead(f_in)
        except IOError as e:
            SysExit(e, 'cannot open file')
    return SimpleCharDet(TryOpen())

def FileInput(filepath):
    with codecs.open(filepath, mode = 'r', encoding = GetCoding(filepath)) as file: return(file.read())

def LogNormalize(logfile):
    log_list = []
    for one_str in logfile.splitlines():
        log_split, log_elem, paren_flag, quote_flag = [], "", False, False
        for one_char in list(one_str):
            if one_char == ' ':
                if not paren_flag and not quote_flag:
                    log_split.append(log_elem)
                    log_elem = ""
                else: log_elem += one_char
            elif one_char == '[': paren_flag = True
            elif one_char == ']': paren_flag = False
            elif one_char == '"': quote_flag = not quote_flag
            else: log_elem += one_char
        if log_elem != "":
            log_split.append(log_elem)
        json = dict(zip(S3Keys(), log_split))
        log_list.append(json)
    return log_list

def LogOutput(dirpath):
    for filename in os.listdir(dirpath):
        try:
            logfile = FileInput(dirpath + filename)
            for s3_log in LogNormalize(logfile):
                CreateRecord(s3_log)
                print(json.dumps(s3_log, sort_keys=True, indent=4))
        except:
            traceback.print_exc()

def S3Keys():
    return ['bucket_owner'
           ,'bucket_name'
           ,'request_datetime'
           ,'remote_ip'
           ,'requesta'
           ,'request_id'
           ,'operation'
           ,'request_key'
           ,'request_uri'
           ,'http_status'
           ,'error_code'
           ,'bytes_sent'
           ,'object_size'
           ,'total_time'
           ,'turn_around_time'
           ,'referrer'
           ,'user_agent'
           ,'version_id']
