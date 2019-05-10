from goslinks.db.factory import model_factory


def run():
    for model_name in ("user", "link"):
        model_factory(model_name).create_table()


if __name__ == "__main__":
    run()
