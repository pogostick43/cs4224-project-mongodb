from pymongo import DESCENDING


def popular_item_transaction(db, w_id, d_id, num_last_orders):
    # Make sure types of data
    w_id = int(w_id)
    d_id = int(d_id)
    num_last_orders = int(num_last_orders)

    # Result
    results = {'w_id': w_id, 'd_id': d_id, 'num_last_orders': num_last_orders}

    # Last L orders
    last_orders = list(db.order.find({"o_w_num": w_id, "o_d_num": d_id}) \
                               .sort('o_num', DESCENDING)[:num_last_orders])

    # Count number of apperance for each item
    count_items = {}
    for order in last_orders:
        for ol in order['o_order_line']:
            count_items[ol['ol_i_num']] = 0 if ol['ol_i_num'] not in count_items else count_items[ol['ol_i_num']]+1

    # Getting results ...
    results['orders'] = []

    for order in last_orders:
        # print order
        popular_items = []
        max_quantity = -1
        for ol in order['o_order_line']:
            if ol['ol_quantity'] > max_quantity:
                popular_items = []
            if ol['ol_quantity'] >= max_quantity:
                popular_items.append({
                    'item_id': ol['ol_i_num'],
                    'quantity': ol['ol_quantity'],
                    'item_name': ol['ol_i_name'],
                    'percentage': float(count_items[ol['ol_i_num']]) / num_last_orders,
                })
                max_quantity = ol['ol_quantity']

        results['orders'].append({
            'info': {
                'order_id': order['o_num'],
                'order_entry_date': order['o_entry_d'],
                'customer_first': order['o_customer']['c_first'],
                'customer_middle': order['o_customer']['c_middle'],
                'customer_last': order['o_customer']['c_last']},
            'popular_items': popular_items})

    return results
