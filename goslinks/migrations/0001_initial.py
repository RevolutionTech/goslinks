from goslinks.db import LinkModel, UserModel


def run():
    UserModel.create_table()
    LinkModel.create_table()


if __name__ == "__main__":
    run()
