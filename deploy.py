# -*- coding: utf-8 -*-
import os
import sys
import time

from app.common.setting import DEBUG

if not DEBUG:
    start_time = time.time()

    deploy_command = 'nuitka --standalone --enable-plugin=pyside6 --debug '
    deploy_command += '--include-package=sqlite3,http.cookies,http.client,hmac,queue,uuid,http '
    # deploy_command += '--windows-disable-console '
    deploy_command += '--msvc=latest '
    deploy_command += '--show-memory --show-progress '
    deploy_command += '--windows-icon-from-ico=app/resource/images/logo.ico '
    deploy_command += '--nofollow-import-to=cgtw2,pipeline_core '
    deploy_command += '--follow-import-to=app '
    deploy_command += '--output-dir=build '
    deploy_command += '--report=build/report.xml '
    deploy_command += 'jumbla.py'
    os.system(deploy_command)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'打包完成，用时： {elapsed_time}')
else:
    print('DEBUG模式下不进行打包')
