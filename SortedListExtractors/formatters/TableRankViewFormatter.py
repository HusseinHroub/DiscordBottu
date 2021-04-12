from tabulate import tabulate

class TableRankViewFormatter:
    def format(self, ranks_data):
        return '```' + tabulate(ranks_data[1:],
                                headers=ranks_data[0],
                                tablefmt="fancy_grid",
                                numalign="left",
                                stralign="left") + '```'
