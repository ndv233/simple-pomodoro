import csv
import datetime
import pandas

# TODO: exporting stats as graphs with matplotlib


FILENAME = 'Stats/stats.csv'  # Name of csv file
current_date = datetime.date.today()
FIELDNAMES = ['date', 'total_time']


def getDate() -> str:
    """
    Gets current date as string in correct format
    :return string:
    """
    date = str(datetime.datetime.today()).split()[0]
    return date


def writeData(session_length: int):
    """
    Writes data into csv file
    :param session_length:
    :return None:
    """
    data = [
        {FIELDNAMES[0]: current_date, FIELDNAMES[1]: session_length}
    ]
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)


def getDataIndex(date: str) -> int:
    """
    Finds and gets row index number of given date inside csv file
    :param date: date to get index for
    :return: row index
    """
    stats_file = pandas.read_csv(FILENAME)
    row_index = stats_file.index.get_loc(stats_file[stats_file[FIELDNAMES[0]] == date].index[0])
    return row_index


def getDataValue(row_index: int) -> int:
    """
    Gets value in total_time column for given row index number
    :param row_index: index of row
    :return: value of total_time in given row
    """
    stats_file = pandas.read_csv(FILENAME)
    val = stats_file.iloc[row_index, 1]
    return val


def overrideData(row_index: int, value: int):
    """
    Writes over current value in total_time column in given row
    :param row_index:
    :param value:
    :return:
    """
    stats_file = pandas.read_csv(FILENAME)
    stats_file._set_value(row_index, FIELDNAMES[1], value)
    stats_file.to_csv(FILENAME, index=False)


def checkData(date: str) -> bool:
    """
    Checks if data for date already exists
    :param date: date to check
    :return: bool
    """
    try:
        stats_file = pandas.read_csv(FILENAME)
        date_column = stats_file[FIELDNAMES[0]].tolist()
        if date in date_column:
            return True
        else:
            return False
    except pandas.errors.EmptyDataError:
        return False


def cumSum(data_list):
    sum_count = 0
    cum_list = []
    for i in data_list:
        sum_count += i
        cum_list.append(sum_count)
    return cum_list

