if ! command -v java &> /dev/null
then
    echo "java could not be found"
    exit
fi
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found"
    exit
fi
if ! command -v sparql &> /dev/null
then
    echo "sparql could not be found"
    exit
fi