class RandomCSV:
    """All of the arguments (meta data) required to initialize randcsv.
    """
    def __init__(
        self,
        rows,
        cols,
        value_length=6,
        output='test.csv',
        data_types=['int'],
        nan_freq=.0,
        empty_freq=.0,
        index_col=False,
        title_row=False,
    ):
        self.rows = rows
        self.cols = cols
        self.value_length = value_length
        self.output = output
        self.data_types = data_types
        self.nan_freq = nan_freq
        self.empty_freq = empty_freq
        self.index_col = index_col
        self.title_row = title_row
