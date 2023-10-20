import os

from numpy import array as np_array
from numpy import fromfile as np_fromfile
from numpy import save as np_save

File_Extension = ".tone"


def normalize_path_exten(file_name: str):
    """adding the tone extension to the file if it does not have one."""
    name, exten = os.path.splitext(file_name)
    if exten != File_Extension:
        file_name += File_Extension
    return file_name


class ToneOPoly:

    __polyfit: np_array = None

    def __init__(self, polyfit: np_array = None):
        self.__polyfit = polyfit

    @property
    def polyfit(self):
        return self.__polyfit

    def save(self, file_name: str):
        file_name = normalize_path_exten(file_name)

        with open(file_name, mode='wb') as file:
            if self.__polyfit is not None:
                file.write(bytearray(self.__polyfit))

    def open(self, file_name: str):

        if os.stat(file_name).st_size == 0:
            self.__polyfit = None
            return

        with open(file_name, mode='rb') as file:
            self.__polyfit = np_fromfile(file, dtype=self.__polyfit.dtype)