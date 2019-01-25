#!/usr/bin/env python

from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from botocore.exceptions import ClientError
import requests
import traceback
import os
import boto3
import inspect
import sys
import random

br = os.environ['BROWSER']
main_url = os.environ['WebURL']
module_table = os.environ['ModuleTable']
status_table = os.environ['StatusTable']
s3_output_bucket = os.environ['ArtifactBucket']
s3 = boto3.client('s3')
s3_path_prefix = os.environ['CODEBUILD_BUILD_ID'].replace(':', '/')


def test_phantomjs():
    phantomjs_function = os.environ['PhantomJSFunction']
    mods = os.environ['MODULES'].split(',')
    client = boto3.client('lambda')
    for mod in mods:
        mod_tcs = ddb.get_item(TableName=module_table, Key={'module': {'S': mod.strip()}})['Item']['testcases']['L']
        for tc in mod_tcs:
            tcname = str(tc['S'].strip())
            try:
                response = client.invoke(ClientContext=tcname, FunctionName=phantomjs_function, InvocationType='Event',
                                         Payload="{\"testcase\": \"" + tcname + "\", \"module\": \"" +
                                         mod.strip() + "\"}")
                print(response)
            except:
                print('Failed while invoking test %s' % tcname)
                traceback.print_exc()
                print(traceback.print_exc())


if __name__ == '__main__':
    if br.lower() == 'chrome':
        browser = webdriver.Chrome()
    elif br.lower() == 'firefox':
        browser = webdriver.Firefox()
    elif br.lower() == 'phantomjs':
        test_phantomjs()
        sys.exit(0)
    else:
        print('Unexpected browser value: %s', br)
        sys.exit(-1)

    if browser:
        browser.quit()
