import sys

from hat.praetorian.relay.main import main


if __name__ == '__main__':
    sys.argv[0] = 'hat-praetorian-relay'
    sys.exit(main())
