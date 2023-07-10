#!/bin/sh

set -e

cd "$(dirname -- "$0")"

PYTHON=python3.8
BIN=/usr/bin
APPLICATIONS=/usr/share/applications
SYSTEM=/etc/systemd/system

VERSION=$(cat VERSION.txt)

if [ $(id -u) -ne 0 ]; then
    echo "Installation should be run as root"
    exit 1
fi

if [ -z $(which $PYTHON 2> /dev/null) ]; then
    echo "Could not find $PYTHON"
    exit 1
fi

echo -n "Installation path [/opt/hat-praetorian]: "
read INSTALL_PATH
[ -z "$INSTALL_PATH" ] && INSTALL_PATH=/opt/hat-praetorian

echo -n "Data path [/var/opt/hat-praetorian]: "
read DATA_PATH
[ -z "$DATA_PATH" ] && DATA_PATH=/var/opt/hat-praetorian

if [ -d $INSTALL_PATH ]; then
    echo -n "Directory $INSTALL_PATH already exists" \
            " - uninstall previous installation? (y/N): "
    read result
    [ "$result" != "y" ] && exit 1
    $INSTALL_PATH/uninstall.sh
fi

echo "Installing Hat PRAETORIAN $VERSION"

mkdir -p $INSTALL_PATH

cat > $INSTALL_PATH/VERSION.txt < VERSION.txt
cat > $INSTALL_PATH/uninstall.sh << EOF
#!/bin/sh
cd "\$(dirname -- "\$0")"
VERSION=\$(cat VERSION.txt)
echo "Uninstalling Hat PRAETORIAN \$VERSION"
unlink $BIN/hat-praetorian-commander
rm $SYSTEM/hat-praetorian-commander.service

rm -r \$(pwd)
EOF
chmod +x $INSTALL_PATH/uninstall.sh

$PYTHON -m venv $INSTALL_PATH
$INSTALL_PATH/bin/pip install -q --no-index packages/*.whl

mkdir -p $DATA_PATH
[ ! -f $DATA_PATH/commander.yaml ] && cat > $DATA_PATH/commander.yaml < commander.yaml
chmod 0666 $DATA_PATH/commander.yaml

ln -sf $INSTALL_PATH/bin/hat-praetorian-commander $BIN/hat-praetorian-commander

mkdir -p $SYSTEM
cat > $SYSTEM/hat-praetorian-commander.service << EOF
[Unit]
Description=Hat PRAETORIAN commander
After=network.target
Requires=network.target

[Service]
WorkingDirectory=$DATA_PATH
ExecStart=$BIN/hat-praetorian-commander

[Install]
WantedBy=multi-user.target
EOF
