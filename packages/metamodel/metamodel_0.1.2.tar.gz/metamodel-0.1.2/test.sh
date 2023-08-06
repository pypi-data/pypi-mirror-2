export PYTHONPATH=$PWD
#TIMEIT=/usr/bin/time

echo "** Namespaces test"
$TIMEIT python test/testns.py
echo "** Hierarchical view system **"
$TIMEIT python test/hierarchical.py
echo "** SubscribableModel tests **"
$TIMEIT python test/simpletest.py
echo "** Dynamicmeta tests **"
$TIMEIT python test/classregistry.py
echo "** Test saving and loading **"
$TIMEIT python test/saveload.py
echo "** Test reference attributes **"
$TIMEIT python test/references.py
echo "** Cross referenced file datasources **"
$TIMEIT python test/filesourcetest.py
echo "** Overlays **"
$TIMEIT python test/overlaytest.py
echo "** Animation **"
$TIMEIT python test/animationtest.py
echo "** Finding functions **"
$TIMEIT python test/testfind.py
