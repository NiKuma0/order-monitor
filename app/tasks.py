from celery import shared_task

from app.views import get_sheet_as_list, sync_sheet_and_db


@shared_task
def test_task():
    rows = get_sheet_as_list()
    sync_sheet_and_db(rows)
