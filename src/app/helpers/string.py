""" String utils """


def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return: Label Value string
    """
    return ': '.join([label, str(value)])
