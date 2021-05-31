set -e

echo "Building pannopi..."

cp -r $SRC_DIR/* $PREFIX/

mkdir $PREFIX/bin
cd $PREFIX/bin
ln -s  $PREFIX/pannopi.py ./pannopi
ln -s  $PREFIX/scripts/pannopi_download_db.py ./pannopi_download_db
chmod +x ./pannopi
chmod +x ./pannopi_download_db
chmod +x ../scripts/config-maker.py
