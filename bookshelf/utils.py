import logging
import math
import os
import random
import string
import time
import uuid

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ErrorResponse:

    @staticmethod
    def build_serializer_error(serializer, status):
        return Response({"status": "error", "errors": serializer.errors},
                        status=status)

    @staticmethod
    def build_text_error(text, status):
        return Response({"status": "error", "errors": text}, status=status)


def random_profile_image_name(instance, old_filename):
    extension = os.path.splitext(old_filename)[1]
    filename = str(uuid.uuid4()) + extension
    return 'profile_images/' + filename


def random_media_name(instance, old_filename):
    extension = os.path.splitext(old_filename)[1]
    filename = str(uuid.uuid4()) + extension
    return 'media/' + filename


def random_thumbnail_name(instance, old_filename):
    extension = os.path.splitext(old_filename)[1]
    filename = str(uuid.uuid4()) + extension
    return 'thumbnails/' + filename


def generate_pin():
    return random.randint(100000, 999999)


def generate_mobile():
    return random.randint(7880000000, 9999999999)


def generate_refrence_number(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' % (math.floor(m), (math.floor(m) - math.floor(m)) * 1000000)
    uniqid = uniqid[6:]
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0, 10, 1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = "{}{}".format(prefix, uniqid)
    return uniqid


def send_sms(number, body):
    """
        Send an SMS message via boto.

        Return True/False if sent.
    """
    sns_client = boto3.client(
        'sns',
        region_name='eu-west-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )  # must be set as bahrain has no SNS.

    try:
        sns_client.publish(
            PhoneNumber=number,
            Message=body,
        )
        return True
    except ClientError as e:
        logger.warning('SNS error sending SMS', extra={'number': number, 'error': e})
        return False
