from sdfspu import csv_data as cd
from sdfspu.sdf_time import stamp_utc_now

processing_timestamp = stamp_utc_now(ms=False)

stripe_csv_path = '/home/pi/Downloads/unified_payments(all).csv'
payments_csv_path = '/home/pi/Downloads/At Home with the Elements Online Event-bookings (2).csv'

# load Stripe data
stripe_data = cd.DataObject()
stripe_data.read_csv(stripe_csv_path)

all_ids_in_stripe_data = []
for row in stripe_data.dict_list:
    all_ids_in_stripe_data.append(
        int(row['order_id (metadata)'])
    )

# load Payment Dashboard data
payment_dash_data = cd.DataObject()
payment_dash_data.read_csv(payments_csv_path)
all_ids_in_payment_dash_data = []
for row in payment_dash_data.dict_list:
    all_ids_in_payment_dash_data.append(
        # str(row['Payer Email'])
        int(row['Order ID'])
    )


if __name__ == "__main__":
    print(f'Processing timestamp:\t{processing_timestamp}')

    print(f'Stripe export csv file:\t{stripe_csv_path}')
    print(stripe_data.info_msg())
    print(f'Number of unique IDs in Stripe:\t{len(set(all_ids_in_stripe_data))}')

    print(f'Payment Dashboard (drupal) csv file:\t{payment_dash_data}')
    print(payment_dash_data.info_msg())
    print(f'Number of unique IDs in Payment Dashboard:\t{len(set(all_ids_in_payment_dash_data))}')

    print('The following are in Stripe, but not in www-site ')
    counter = 0
    for this_stripe_id in all_ids_in_stripe_data:
        if this_stripe_id not in all_ids_in_payment_dash_data:
            counter += 1
            print(this_stripe_id)
    print(f'\nHow many in Stripe but not in www-site: {counter}\n\n')

    print('The following are in Stripe, AND in www-site ')
    counter = 0
    for this_stripe_id in all_ids_in_stripe_data:
        if this_stripe_id in all_ids_in_payment_dash_data:
            counter += 1
            print(this_stripe_id)

    print(f'\nHow many in Stripe AND in www-site: {counter}\n\n')

