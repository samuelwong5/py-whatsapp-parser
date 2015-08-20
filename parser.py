# -*- coding: utf-8 -*- 
import operator
import re
import sys


def parse_messages(key=''):
    msg_dict = {}    
    total_msg = 0    
    for msg in messages:
        m = msg.split('\n')
        if ':' in m[0]:
            usr = m[0].split(':')[0]
            m = filter(lambda x: key in x, m)
            total_msg += len(m) - (1 if key=='' else 0)
            try:
                msg_dict[usr] = msg_dict[usr] + len(m) - (1 if key=='' else 0)
            except:
                msg_dict[usr] = len(m) - (1 if key=='' else 0)
    return msg_dict, total_msg

    
def message_print_count(data, sort=True):
    msg_dict, total_msg = data
    row_format ='{:<25}{:>6}{:>7}'
    print row_format.format('User', *['Msgs', '%'])
    if sort:
        msg_dict = sorted(msg_dict.items(), key=lambda x: x[1], reverse=True)
        for usr, count in msg_dict:
            print row_format.format(usr, *[count, str(count * 100 / total_msg) + '%'])
    else:
        for usr, count in msg_dict.iteritems():
            print row_format.format(usr, *[count, str(count * 100 / total_msg) + '%'])
    print('Total: ' + str(total_msg))
    
    
if __name__ == "__main__":    
    f = None
    with open(sys.argv[1]) as file:
        f = file.read()

    # Get start-end date range
    dates = f.split('\n')
    msg_start = dates[0].split(' - ')[0]
    msg_end = ''
    for i in range(len(dates)-1, -1, -1):
        msg_end = dates[i]
        if ' - ' in msg_end:
            msg_end = msg_end.split(' - ')[0]
            break
    print('\nFrom: ' + msg_start + '\nTo: ' + msg_end + '\n')
    
    messages = re.split('\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2} - ', f)
    msg_dict = {}    
    
    if not '--no-total' in sys.argv:
        print('Total Messages:')
        message_print_count(parse_messages())
     
    try:
        i = sys.argv.index('--keyword') + 1
        while ('--' not in sys.argv[i]):
            print('\nMessages containing "' + sys.argv[i] + '":')
            message_print_count(parse_messages(sys.argv[i]))
            i += 1
    except:
        pass
        
    if '--media' in sys.argv:
        print('\nMedia sent:')
        message_print_count(parse_messages('<Media omitted>'))
