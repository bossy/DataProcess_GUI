#!/usr/bin/env python3

import utm
import pandas as pd
import os
from os.path import expanduser
import sys
from pandas.errors import ParserError


class Utm2latlon():
    """
    Inputs a .CSV or Excel file with UTM (easting and northing) coordinates
    and outputs a .CSV file (..._output.csv) with corresponding latitude and
    longitude coordinates as new columns.
    Arguments:
         file_path: Absolute or relative path of .CSV file
         zone_number: UTM zone number
         zone_letter: UTM zone letter

    """

    def __init__(self, file_path: str, zone_number: int, zone_letter: str):
        self.file_path = expanduser(file_path)
        self.dir_, self.file_name = os.path.split(self.file_path)
        self.basename, self.ext = os.path.splitext(self.file_name)
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.df = None
        self.read_file()

    def read_file(self):
        """
        Reads CSV or Excel file in a pandas dataframe. Exceptions exist
        if the file is not found or is not readable by pandas.
        :return:
        """

        if self.ext.lower() == ".csv":
            try:
                self.df = pd.read_csv("{}".format(self.file_path))
            except ParserError:
                print("ERROR: File must be a CSV or Excel file.")
            except FileNotFoundError:
                print("ERROR: File does not exist!!!")
            else:
                self.convert(self.df)
        elif (self.ext.lower() == ".xls" or
              self.ext.lower() == ".xlsx"):
            try:
                self.df = pd.read_excel("{}".format(self.file_path))
            except ParserError:
                print("ERROR: File must be a CSV or Excel file.")
            except FileNotFoundError:
                print("ERROR: File does not exist.")
            else:
                self.convert(self.df)
        else:
            print("ERROR: File must be a CSV or Excel file.")

    def convert(self, df_convert):
        """
        Converts data using the utm package and creates new "latitude" and
        "longitude" columns within the dataframe.
        :param df_convert:
        :return:
        """
        try:
            for index, row in df_convert.iterrows():
                easting = row.easting
                northing = row.northing
                utm_lat, utm_lon =\
                    utm.to_latlon(easting, northing, self.zone_number, self.zone_letter)
                df_convert.loc[index, 'latitude'] = utm_lat
                df_convert.loc[index, 'longitude'] = utm_lon
            self.write_file(df_convert)
        except AttributeError:
            print("Error: File requires \"easting\" and \"northing\" column headings (lower case).")

    def write_file(self, df_write):
        """
        Writes dataframe to disk.
        :param df_write:
        :return:
        """

        output_file = os.path.join(self.dir_, self.basename + "_output" + ".csv")
        df_write.to_csv(output_file, index=False)
        print("Output: " + output_file)


#  Arguments for when the program is run in the command line.

if __name__ == "__main__":
    Utm2latlon(sys.argv[1], int(sys.argv[2]), sys.argv[3])
