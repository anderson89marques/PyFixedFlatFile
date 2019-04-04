class ParamsException(Exception):
    """Exception raised when tp, fmt and size values are wrongs"""
    pass


class LineSizeException(Exception):
    """Exception raised when line size is bigger then specified"""
    pass


class LineIdentifierException(Exception):
    """Exception raised when line indentifier rased from the
    file is different to the line identifier used in the specification

    obs: line identifier is defined using .eq() function 
    """
    pass
