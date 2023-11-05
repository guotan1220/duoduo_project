from django.conf import settings
from authlib.jose import jwt, JoseError

def generate_verify_email_url(user):
    """生成用于邮箱验证的JWT（json web token）"""
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = settings.SECRET_KEY
    # 待签名的数据负载
    data = {'user_id': user.id, 'email': user.email}
    token = jwt.encode(header=header, payload=data, key=key).decode()
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url

def check_verify_email_token(token):
    return jwt.decode(token, key=settings.SECRET_KEY)
