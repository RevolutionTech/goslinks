from goslinks.db.factory import get_model


def run():
    for model_name in ("user", "link"):
        get_model(model_name).create_table()


if __name__ == "__main__":
    run()
