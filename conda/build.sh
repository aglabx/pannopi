set -e

echo "Building pannopi..."

cp -r $SRC_DIR/* $PREFIX/

cd $PREFIX/bin

chmod +x ./*

chmod +x ../scripts/config-maker.py