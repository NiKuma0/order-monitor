import datetime
from time import time

from django.test import TestCase

from app.views import sync_sheet_and_db
from app.models import Order


class SyncSheetAndDbTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.function = sync_sheet_and_db
        return super().setUpClass()

    def setUp(self) -> None:
        self.rows = [
            [str(i), str(100*i), str(37*i), '24.02.2022'] for i in range(50)
        ]
        self.startTime = time()

    @property
    def typed_rows(self):
        return [
            (int(row[0]), int(row[1]), int(row[2]),
             datetime.datetime.strptime(row[3], '%d.%m.%Y').date())
            for row in self.rows
        ]

    def test_create(self, test_created=True):
        count_created = SyncSheetAndDbTest.function(
            self.rows
        )

        if test_created:
            self.assertEqual(
                count_created, len(self.rows)
            )
            self.assertEqual(
                Order.objects.count(), count_created
            )
        self.assertEqual(
            list(Order.objects.all().values_list()), self.typed_rows
        )

    def test_2x_create(self):
        self.test_create()
        self.test_create(False)

    def test_update(self):
        self.test_create()
        first_row = self.rows[0]
        first_row = [first_row[0], first_row[1] + '1', first_row[2] + '1', first_row[3]]
        SyncSheetAndDbTest.function(
            self.rows
        )
        self.assertEqual(
            list(Order.objects.filter(id=self.typed_rows[0][0]).values_list()), [self.typed_rows[0]]
        )

    def test_delete(self):
        self.test_create()
        must_deleted = self.rows.pop(-1)
        SyncSheetAndDbTest.function(
            self.rows
        )
        self.assertRaises(Order.DoesNotExist, Order.objects.get, id=must_deleted[0])

    def tearDown(self) -> None:
        print('\n%s: %.3f' % (self.id(), time() - self.startTime))
        Order.objects.all().delete()
        return super().tearDown()
