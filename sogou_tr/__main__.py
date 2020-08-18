import sys
from .sogou_tr import sogou_tr

print('__main__')
print('__main__.__name__', __name__)
print('__main__.__package__', __package__)

print('sys.path', sys.path)

sogou_tr.main()