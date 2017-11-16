from .tables import Cell


def debug_print_cell_grid(cells):
    for cell_line in cells:
        result_line = ["" for _ in range(5)]
        for cell in cell_line:
            rf = Cell.reverse_long_format

            left0, top0, right0, bottom0 = (rf[cell.styles.left],
                                            rf[cell.styles.top],
                                            rf[cell.styles.right],
                                            rf[cell.styles.bottom])

            left1, top1, right1, bottom1 = (rf[cell.neighbours.left.styles.right],
                                            rf[cell.neighbours.top.styles.bottom],
                                            rf[cell.neighbours.right.styles.left],
                                            rf[cell.neighbours.bottom.styles.top])

            result_line[0] += "    %s       " % top1
            result_line[1] += "    %s       " % top0
            result_line[2] += "%s %s   %s %s   " % (left1, left0, right0, right1)
            result_line[3] += "    %s       " % bottom0
            result_line[4] += "    %s       " % bottom1

        for l in result_line:
            print(l)
        print()
