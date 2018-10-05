import argparse
from tools import Scanner

def main():
    # Init parser
    parser = argparse.ArgumentParser(usage='%(prog)s [options]', description='Basic port scanner with cmd line handler')

    # Add arguments
    parser.add_argument('-t', '--target', type=str, default='w3c.com',
                        help='Set target. (default: w3c.pl)')
    parser.add_argument('-w', '--workers', type=int, default=300,
                        help='How many thread to create? (default: 300)')
    parser.add_argument('-r', '--range', type=int, default=1000,
                        help='How many ports to scan? (default: 1000)')
    parser.add_argument('-k', '--known', action='store_true',
                        help='Scan only known ports. (default: False)')
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType('r'), default='ports.json',
                        help='Import your own json with ports description. (default: ports.json)')
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('a'), default='out.txt',
                        help='Set output file. Append mode. (default: out.txt)')

    # Parse arguments to args
    args = parser.parse_args()

    # Prepare scanner object
    scan = Scanner(args.target, args.workers, args.known, args.range, args.input, args.output)

    # Clear arguments
    del args

    # Start Scan
    scan.run()

if __name__ == '__main__':
    main()
