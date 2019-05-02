from goslinks.db import LinkModel, UserModel


def run():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1)
    LinkModel.create_table(read_capacity_units=1, write_capacity_units=1)


if __name__ == '__main__':
    run()
