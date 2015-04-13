# -*- coding: utf-8 -*-
import math
import applogger
import re
import sys
from getch import getch
from simplestore import SimpleStorage

logger = applogger.getLogger("MatrixCalculator")

class ConsoleMatrixCalculator(object):
    
    def __init__(self):
        self._storage = SimpleStorage()
        self._storage.load_from_disk()
        self._storage_prefix = "matrix:"
        self._getstore_name = lambda name: self._storage_prefix + name

    def two_matrix_op(self, m1, m2, callback):
        results = []
        logger.debug("Matrix Operation Start...")
        for i, arr in enumerate(m1):
            result = []
            for j, el in enumerate(arr):
                result.append(callback(m1, m2, i, j))
            results.append(result)
        logger.debug("Matrix Operation End...")
        return results

    def matrix_add(self, m1, m2):
        size1 = self.matrix_size(m1)
        size2 = self.matrix_size(m2)
        assert size1 == size2, "Matrix(%d,%d) Add Matrix(%d,%d) is not defined." (size1+size2)
        def add(m1, m2, i, j):
            v1 = m1[i][j]
            v2 = m2[i][j]
            sum = v1 + v2
            logger.debug("%d + %d = %d position (%d, %d)" % (v1, v2, sum, i, j))
            return sum
        return self.two_matrix_op(m1, m2, add) 
    
    def matrix_substract(self, m1, m2):
        size1 = self.matrix_size(m1)
        size2 = self.matrix_size(m2)
        assert size1 == size2, "Matrix(%d,%d) Substract Matrix(%d,%d) is not defined." (size1+size2)
        def sub(m1, m2, i, j):
            v1 = m1[i][j]
            v2 = m2[i][j]
            dif = v1 - v2
            logger.debug("%d - %d = %d position (%d, %d)" % (v1, v2, dif, i, j))
            return dif
        return self.two_matrix_op(m1, m2, sub) 

    def matrix_multiply_constant(self, m1, constant):
        def multiply(m1, m2, i, j):
            v1 = m1[i][j]
            v2 = m2
            ret = v1 * v2
            logger.debug("%d * %d = %d position (%d, %d)" % (v1, v2, ret, i, j))
            return ret
        return self.two_matrix_op(m1, constant, multiply)

    def matrix_power(self, m1, power):
        assert power > 0, "Power must greater than 0."
        temp = m1
        for n in xrange(power-1):
            temp = self.matrix_multiply(temp, m1)
        return temp

    def matrix_multiply(self, m1, m2):
        size1 = self.matrix_size(m1)
        size2 = self.matrix_size(m2)
        assert size1[1] == size2[0], "Matrix(%d,%d) Multiply Matrix(%d,%d) is not defined." (size1+size2)
        def multiply(m1, m2, i, j):
            sum = 0
            tpl = "%d*%d"
            log = []
            for x in xrange(len(m1[0])):
                v1 = m1[i][x]
                v2 = m2[x][j]
                sum += v1*v2
                log.append(tpl % (v1, v2))
            logger.debug(" + ".join(log) + " = %d position (%d, %d)" % (sum, i, j))
            return sum
        return self.two_matrix_op(m1, m2, multiply)

    def matrix_size(self, matrix):
        assert len(matrix) > 0, "Matrix's row cant be less than zero"
        assert len(matrix[0]) > 0, "Matrix' column cant be less than zero"
        return len(matrix), len(matrix[0])

    def input_matrix(self):
        print "Please Input a matrix:"
        print "(use <space> or <comma> to split numbers)"
        print "(use a empty line means end input)"
        line_data = ""
        matrix = []
        last_line = ""
        while True:
            line_data = raw_input()
            if not line_data:
                break
            try:
                line_array = self._parse_matrixline(line_data)
            except ValueError:
                print "Errors are occurred when parsing your inputs"
                print "probably your inputs have non-digit character"
                print "please check it, and input again."
                continue

            if last_line:
                if len(last_line) != len(line_array):
                    print "the length of elements you just input not equal the last line, please input this line again."
                    continue
            last_line = line_array
            matrix.append(line_array)
        print "your matrix has been successfully recieved."
        print "your matrix is shown as below:"
        self.print_matrix(matrix)
        return matrix
    
    def save_matrix(self, matrix):
        print "Please input a name for the matrix in order to save it"
        while True:
            line_data = raw_input()
            name = self._getstore_name(line_data.strip())
            if name in self._storage._dicts:
                print "this name has already been taken, please change one"
                continue
            self._storage._dicts[name] = matrix
            self._storage.save_to_disk()
            print 'matrix "%s" has been saved.' % line_data.strip()
            return

    def list_saved_matrix(self):
        print "These are matrices has been saved in storage:"
        for k, m in self._storage._dicts.iteritems():
            if k.startswith("matrix:"):
                print 'Matrix: "%s"' % "".join(k.split(":")[1:])
                self.print_matrix(m)
                print ""

    def get_matrix_byname(self, name):
        matrixname = self._getstore_name(name)
        return self._storage._dicts[matrixname]

    def remove_matrix_byname(self, name):
        matrixname = self._getstore_name(name)
        while True:
            print 'Are you sure to remove matrix "%s" ?' % name
            try:
                self.print_matrix(self.get_matrix_byname(name))
            except KeyError, e:
                print "the matrix acctually does not exists in storage."
                return
            self._std_write("(y/n?)")
            answer = raw_input().strip()
            if(answer == 'y'):
                del self._storage._dicts[matrixname]
                self._storage.save_to_disk()
                print 'matrix "%s" has been removed' % name
            else:
                print 'cancelled.'
            return

    def _get_max_min_number(self, matrix):
        max_number = 0
        min_number = sys.maxint
        for arr in matrix:
            for el in arr:
                if el > max_number:
                    max_number = el
                if el < min_number:
                    min_number = el
        return min_number, max_number

    def _std_write(self, obj):
        sys.stdout.write(obj)

    def _longest_numberlength(self, matrix):
        min_num, max_num = self._get_max_min_number(matrix)
        minlog = 0 if min_num == 0 else math.floor(math.log10(abs(min_num)))
        maxlog = 0 if max_num == 0 else math.floor(math.log10(abs(max_num)))
        negate = 0
        if minlog >= maxlog:
            negate = 1
        return int(max(minlog, maxlog)) + negate + 1 

    def _get_default(self, name, default, options):
        return default if not name in options else options[name]

    def print_matrices_inline(self, *matrices, **options):
        num = self._get_default('num', 3, options)
        group_matrices = self._group_matrices(num, *matrices)
        delim = self._get_default("delim", "\t", options)
        place_holder = self._get_default('place_holder', " ", options)
        newline = self._get_default("newline", '\n', options)
        desc = self._get_default("desc", "", options)
        for group in group_matrices:
            mg_sizes = map(lambda x: self.matrix_size(x), group)
            max_row = max(mg_sizes, key=lambda x:x[0])[0]
            group_col = map(lambda x: x[1], mg_sizes)
            for row in xrange(max_row):
                for m in group:
                    length = self._longest_numberlength(m)
                    if row == 0 or row == max_row-1:
                        self._std_write("- ")
                    else:
                        self._std_write("| ")
                    for c in xrange(len(m[0])):
                        if row >= len(m):
                            self._std_write(place_holder)
                        else:
                            self._std_write(("%" + str(length) + "s ") % m[row][c])
                    if row == 0 or row == max_row-1:
                        self._std_write("-")
                    else:
                        self._std_write("|")
                    self._std_write(delim)
                    if desc:
                        self._std_write(desc)
                        desc = " " * len(desc)
                    self._std_write(delim)
                self._std_write(newline)
            self._std_write(newline)

    def _group_matrices(self, num, *matrices):
        grouped = []
        group = []
        for i, m in enumerate(matrices):
            if i != 0 and i % num == 0:
                grouped.append(group)
                group = []
            group.append(m)
        if group:
            grouped.append(group)
        return grouped

    def print_matrix(self, matrix):
        length = self._longest_numberlength(matrix)
        for i, arr in enumerate(matrix):
            if i == 0 or i == (len(matrix) - 1):
                self._std_write("- ")
            else:
                self._std_write("| ")
            for el in arr:
                self._std_write(("%" + str(length) + "s ") % el)
            if i == 0 or i == (len(matrix) - 1):
                self._std_write("-")
            else:
                self._std_write("|")
            self._std_write("\n")

    def _parse_matrixline(self, line_str):
        str_array = re.split("[, ;]+", line_str)
        logger.debug("raw input:" + line_str)
        logger.debug("parsed array" + str(str_array))
        if not str_array[-1]:
            str_array.pop()
        return map(lambda el: int(el), str_array)

if __name__ == "__main__":
    """matrix calculator for python execise"""
    matrix = [[0,0,1,0], [1,2,-3,4],[2,1,4,0],[1,2,-3,0]]
    cmc = ConsoleMatrixCalculator()
    cmc.print_matrices_inline(matrix, cmc.matrix_power(matrix, 4), desc=u" →  power 4  →"  )
#    cmc.print_matrix(matrix)
#    ret = cmc.matrix_power(matrix, 4)
#    cmc.print_matrix(ret)
#    print cmc._longest_numberlength(matrix)
#    inputs = cmc.input_matrix()
#    cmc.save_matrix(inputs)
#    cmc.list_saved_matrix()
#    em = cmc.get_matrix_byname("exec2")
#    cmc.print_matrix(cmc.matrix_power(em, 2))
#    cmc.print_matrix(cmc.matrix_power(em, 3))
#    cmc.print_matrix(cmc.matrix_power(em, 4))
#    cmc.print_matrix(cmc.matrix_power(em, 5))
#    cmc.print_matrix(cmc.matrix_power(em, 6))
#    cmc.print_matrix(cmc.matrix_power(em, 7))
