for name in *.py; do
    python -m unittest -v ${name/.py/}
done