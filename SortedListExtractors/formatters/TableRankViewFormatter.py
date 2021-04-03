from terminaltables import SingleTable


class TableRankViewFormatter:
    def format(self, ranks_data):
        table = SingleTable(ranks_data)
        table.inner_heading_row_border = False
        table.inner_row_border = True
        return '```' + table.table + '```'
