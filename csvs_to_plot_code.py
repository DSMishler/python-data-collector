import sys
import pdcutils

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        target = sys.argv[1]
    else:
        target = "."
    pdcutils.generate_plot_code(target)
