set -e

echo "Building pannopi..."

cp -r $SRC_DIR/* $PREFIX/

chmod +x ../scripts/config-maker.py
