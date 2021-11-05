#!/bin/sh

set -e

celery -A api worker -l error -B --scheduler django_celery_beat.schedulers:DatabaseScheduler &

