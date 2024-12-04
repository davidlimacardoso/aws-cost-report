#!/usr/bin/env python3

import boto3, os, click
from calendar import monthrange
from datetime import datetime
from prettytable import PrettyTable

# Make the table with PrettyTable
def create_pretty_table():
    table = PrettyTable(
        field_names=['Period', 'Account', 'Service', 'Amount'],
        border=True,
        header=True,
        align='l',
        padding_width=1
    )
    table.align["Amount"] = "r"
    return table

def get_cost_and_usage(client, start, end):
    """
    Retrieve AWS cost and usage data for the specified time period.
    
    Args:
        client: Boto3 cost explorer client
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        
    Returns:
        List of cost and usage results
    """
    results = []
    
    while True:
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ],
        )
        results += response['ResultsByTime']
        if 'NextPageToken' not in response:
            break
    
    return results

# Format date to month and year eg: Nov 2024
def format_month_year(date_str):
    """Return formatted date string."""
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%b %Y')

# Output file method
def output_file(out, pretty) -> None:
    """Write the output to a file."""

    # Create dir 'result/' if not exist
    os.makedirs('result', exist_ok=True)

    if out == "csv":
        with open("./result/output" + ".csv", 'w') as f:
            f.write(str(pretty.get_csv_string()))
    elif out == "html":
        with open("./result/output"  + ".html", 'w') as f:
            f.write(str(pretty.get_html_string()))
    elif out == "json":
        with open("./result/output"  + ".json", 'w') as f:
            f.write(str(pretty.get_json_string()))
    elif out == "text":
        with open("./result/output"  + ".txt", 'w') as f:
            f.write(str(pretty.get_string()))
    else:
            exit("No output file specified (json, html, csv or text)")

def fill_table_content(pretty, results, only_total):
    """Fill the PrettyTable with AWS cost data."""
    total = 0

    for result_by_time in results:
        total_month = 0

        for group in result_by_time['Groups']:
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            if amount < 0.00001:
                continue
            
            total += amount
            total_month += amount
            
            if not only_total:
                pretty.add_row([
                    format_month_year(result_by_time['TimePeriod']['Start'])
                    ,group['Keys'][0]
                    ,group['Keys'][1]
                    ,format(amount, '0.2f')
                ])

        # Add total row
        pretty.add_row([
            f'Total {format_month_year(result_by_time["TimePeriod"]["Start"])}'
            ,group["Keys"][0]
            ,'ALL SERVICES'
            ,format(total_month, "0.2f")
        ], divider=True)
    
    # Add Total amount between period
    if len(results) > 1:
        pretty.add_row([
            'Total'
            ,group["Keys"][0]
            ,'TOTAL ALL SERVICES PERIOD'
            ,format(total, "0.2f")
        ], divider=True )

# Input options
@click.command()
@click.option('-p', '--profile', help='Use the AWS profile name (optional)')
@click.option('-s', '--start', help='Start date YYYY-MM-DD (default: 1st date of current month)')
@click.option('-e', '--end', help='End date YYYY-MM-DD (default: last date of current month)')
@click.option('--only-total', is_flag=True, default=False, help='Show only total by month and year')
@click.option('--out', help='Choose the output file options (json, html, csv or text)')
def report(profile, start, end, only_total, out):
    """Generate an AWS cost report."""
    try:
        # Set start/end to current month if not specified
        if not start or not end:
            ldom = monthrange(datetime.today().year, datetime.today().month)[1]
            start = datetime.today().replace(day=1).strftime('%Y-%m-%d')
            end = datetime.today().replace(day=ldom).strftime('%Y-%m-%d')

        # Cost explorer client SDK
        ce = boto3.Session(profile_name=profile).client('ce')
        results = get_cost_and_usage(ce, start, end)

        # Create and fill table
        pretty = create_pretty_table()
        fill_table_content(pretty, results, only_total)

        if out: output_file(out, pretty)

        # Print the table
        print(pretty)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    report()