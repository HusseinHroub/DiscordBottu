from tabulate import tabulate

class TabularStringFormatter:
    def format(self, ranks_data, tablefmt='fancy_grid'):
        return '```' + tabulate(ranks_data[1:],
                                headers=ranks_data[0],
                                tablefmt=tablefmt,
                                numalign="left",
                                stralign="left") + '```'
