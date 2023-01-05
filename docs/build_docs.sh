echo "Purging source/generated/** ."
rm -rf source/generated/
echo "source/generated/** purged."

poetry run make clean
poetry run make html
