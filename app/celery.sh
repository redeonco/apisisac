#!/bin/sh

set -e

celery -A api worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler &

