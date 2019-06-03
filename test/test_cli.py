from unittest import mock

from goslinks.cli import migrate
from goslinks.db.factory import get_model, get_models
from test.app_test_case import SimpleTestCase


class MigrateTestCase(SimpleTestCase):
    def setUp(self):
        self.runner = self.app.test_cli_runner()

    def tearDown(self):
        for model in get_models():
            model.delete_table()

    def test_migrate_creates_tables(self):
        user_model = get_model("user")
        link_model = get_model("link")
        self.assertFalse(user_model.exists())
        self.assertFalse(link_model.exists())

        result = self.runner.invoke(migrate, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            "Creating table goslinks-users... SUCCESS!\nCreating table goslinks-links... SUCCESS!\n",
        )

        self.assertTrue(user_model.exists())
        self.assertTrue(link_model.exists())

    @mock.patch(
        "goslinks.cli.get_model",
        return_value=mock.Mock(
            Meta=mock.Mock(table_name="goslinks-users"),
            create_table=mock.Mock(side_effect=ValueError),
        ),
    )
    def test_migrate_outputs_failed_on_failure(self, mock_get_model):
        result = self.runner.invoke(migrate)
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, "Creating table goslinks-users... FAILED!\n")
