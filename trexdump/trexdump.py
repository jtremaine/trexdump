import sys
import argparse

description = \
"""
Trex dump display a compressed, human-readable version of file contents.
"""

class OutputData:
    """
    Compressed version of file data formatted for output.
    """
    output_string = ""
    first_data = True

    # TODO: Use the data width to format the output?
    data_width = 1

    def print_data(self):
        print self.output_string

    def insert(self, data, count):
        if not self.first_data:
            self.output_string += "\n"
        self.output_string += ("%s%d" % (data, count))
        self.first_data = False

    def __init__(self, data_width):
        self.data_width = data_width

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-w', '--data-width', default=1, type=int,
                        help='Width of data element in bytes.')
    parser.add_argument('file', help='File input.')
    args = parser.parse_args()

    # Open the input file
    try:
        fd = open(args.file, 'r')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return

    output_data = OutputData(args.data_width)

    # Read the input file one unit of data at a time
    out_string = ""
    cur_data = None
    cur_data_count = 0
    while 1:
        byte_s = fd.read(args.data_width)
        if not byte_s:
            break

        if cur_data == None:
            cur_data = byte_s
            cur_data_count = 1
        elif byte_s == cur_data:
            cur_data_count += 1
        else:
            output_data.insert(cur_data, cur_data_count)
            cur_data = byte_s
            cur_data_count = 1

    fd.close()

    if cur_data != None:
        output_data.insert(cur_data, cur_data_count)

    output_data.print_data()

if __name__ == "__main__":
    main()
