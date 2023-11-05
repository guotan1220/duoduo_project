#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery_demo.tasks import celery_send_sms_code
mobile = 18687529472
code = '1213'
celery_send_sms_code.delay(mobile, code, 2)