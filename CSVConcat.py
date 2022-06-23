import os
import csv
import sys

from os.path import basename


class CSVConcatenator:
    def __init__(self, source_path, destination_file):
        self.source_path = source_path
        self.destination_file = destination_file
        self.csv_generator = self._get_csv_files(source_path)

    # wrote a recursive descent here rather than os.walk as I specifically want full paths of csv files
    # makes later code nicer - this should be the only complex thing going on as it's really a recursive generator
    # this saves us loading all the file paths into memory at once - no idea how many you might have...
    def _get_csv_files(self, path):
        dir_entry = os.scandir(path)

        # note I'm ignoring symlinks and hard-coding the file extension I want
        for thing in dir_entry:
            if thing.is_dir():
                yield from self._get_csv_files(thing.path)

            if thing.is_file() and '.csv' in thing.name:
                yield thing.path

    # public functions consume the file name generator, they shouldn't call each other
    def list_files(self):
        for x in self.csv_generator:
            print(x)

    def concat_files(self):
        with open(self.destination_file, "w") as writer_file:
            written_header = False

            csv_writer = csv.writer(writer_file)

            for file in self.csv_generator:
                with open(file, "r") as opened_file:
                    csv_reader = csv.reader(opened_file, dialect=csv.excel)

                    # once we wrote a header skip the 1st row of all subsequent files
                    if written_header:
                        next(csv_reader)

                    for row in csv_reader:
                        # add the path to the row to know from whence it came
                        new_row = row + [file]

                        # only write the header for the first row and include an extra column to store the path
                        if not written_header:
                            new_row = row + ["path"]
                            written_header = True

                        csv_writer.writerow(new_row)


def main():
    if len(sys.argv) < 2:
        print("CSV Concatenator thing for Amanda\n")

        print("Concatenate CSV files split across arbitrarily deeply nested subdirectories. Assumes headers are the "
              "same across files. ")

        print("If you parse just the path to the directory the files that will be processed are listed, if you pass the "
              "output file then those files will be concatenated into the new location\n")

        print(f"Usage: python3 {basename(sys.argv[0])} [path to data] [full path to output file including filename]")

        return 0

    concat = CSVConcatenator(sys.argv[1], None if len(sys.argv) == 2 else sys.argv[2])

    if len(sys.argv) == 2:
        concat.list_files()
    else:
        concat.concat_files()


if __name__ == '__main__':
    main()


