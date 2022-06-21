import os
from os.path import join
import csv


def concat_files(root_csv_path, outputfile_with_path):
    things = os.walk(root_csv_path)

    written_header = False

    with open(outputfile_with_path, "w") as writer_file:
        csv_writer = csv.writer(writer_file)

        for root, dirs, files in things:
            for file in files:
                if "csv" in file:
                    filepath = join(root, file)
                    with open(filepath, "r") as opened_file:
                        csv_reader = csv.reader(opened_file, dialect=csv.excel)

                        if written_header:
                            next(csv_reader)

                        for row in csv_reader:
                            new_row = row + [filepath]

                            if not written_header:
                                new_row = row + ["path"]
                                written_header = True

                            csv_writer.writerow(new_row)


if __name__ == '__main__':
    concat_files("/home/justin/csvfiles", "/home/justin/concat.csv")


