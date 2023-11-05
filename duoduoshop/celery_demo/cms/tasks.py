
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery_demo.main import cel
from Libs.yuntongxun.sms import CCP
import logging
logger = logging.getLogger('django')
@cel.task(name='celery_send_sms_code')
def celery_send_sms_code(mobile, sms_code, expires):
    print('runing...')
    try:
        res = CCP().send_template_sms(mobile, [sms_code, expires], 1)
    except Exception as e:
        logger.error('error: mobile: %s sms_code: %s' % (mobile, sms_code))
    else:
        if res != 0:
            # ���Ͷ���ʧ��
            logger.error('failue: mobile: %s sms_code: %s' % (mobile, sms_code))
        else:
            # ���Ͷ��ųɹ�
            logger.info('sucess: mobile: %s sms_code: %s' % (mobile, sms_code))
