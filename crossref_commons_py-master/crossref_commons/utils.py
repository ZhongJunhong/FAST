def to_filter_string(filter):
    return ','.join(['{}:{}'.format(k, v) for k, v in filter.items()])


def parse_filter_string(filter_text):
    if filter_text is None or not filter_text:
        return {}
    return {f.split(':')[0]: f.split(':')[1] for f in filter_text.split(',')}
