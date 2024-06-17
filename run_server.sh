pkill -9 python
hmcoffee="/home/adam/HM/odoo-hmcoffee/addons"
for var in "$@"
do
hmcoffee="${hmcoffee},/home/adam/HM/odoo-hmcoffee/$1"
done

echo $hmcoffee;

./odoo-bin --log-level=debug --addons-path=$hmcoffee -d coba --db_port 5432 --xmlrpc-port=8070  --limit-memory-hard 0 --limit-time-real=10000 -u coba
# ./odoo-bin --addons-path=$hmcoffee -d hmcoffee --db_port 5432 --xmlrpc-port=8070  --limit-memory-hard 0 --limit-time-real=10000 -i base
