class SimpleRankViewFormatter:
    def format(self, ranks_data):
        formatted_text = ''
        stat_type = ranks_data[0][2]
        for row in ranks_data[1:]:
            formatted_text += f'{row[0]}- {row[1]} with {row[2]} {stat_type}\n\n'
        return formatted_text


