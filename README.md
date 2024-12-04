# AWS Cost Explorer Pretty Report written in Python

## Prerequisites

- Python 3.10 (or later)


## Install Requirements
```bash
$ pip install -r requirements
```

## Usage

### Show Help 

```bash
$ ./aws-cost-explorer-report-cli.py --help
Usage: aws-cost-explorer-report-cli.py [OPTIONS]

  Generate an AWS cost report.

Options:
  -P, --profile TEXT  Use the AWS profile name (optional)
  -S, --start TEXT    Start date YYYY-MM-DD (default: 1st date of current month)
  -E, --end TEXT      End date YYYY-MM-DD (default: last date of current month)
  --only-total        Show only total by month and year
  --out TEXT          Choose the output file options (json, html, csv or text)
  --help              Show this message and exit.
```

## Examples

Check cost explorer report of date range [2024-10-01,2024-11-30]

```bash
$ ./aws-cost-explorer-report-cli.py -s 2024-10-01 -e 2024-11-30
+----------------+--------------+-------------------------------------------------+---------+
| Period         | Account      | Service                                         |  Amount |
+----------------+--------------+-------------------------------------------------+---------+
| Oct 2024       | 893777461466 | AWS CloudTrail                                  |    0.26 |
| Oct 2024       | 893777461466 | AWS Config                                      |   10.47 |
| Oct 2024       | 893777461466 | AWS Key Management Service                      |   26.81 |
| Oct 2024       | 893777461466 | AWS Lambda                                      |    0.00 |
| Oct 2024       | 893777461466 | Amazon Virtual Private Cloud                    |   84.75 |
| Oct 2024       | 893777461466 | AmazonCloudWatch                                |   13.64 |
| ..........     | ............ | .................                               |    .... |
| Oct 2024       | 893777461466 | CodeBuild                                       |    0.18 |
| Oct 2024       | 893777461466 | Tax                                             |  115.88 |
| Total Oct 2024 | 893777461466 | ALL SERVICES                                    | 1057.24 |
+----------------+--------------+-------------------------------------------------+---------+
| Nov 2024       | 893777461466 | AWS CloudTrail                                  |    0.18 |
| Nov 2024       | 893777461466 | AWS Config                                      |   68.14 |
| Nov 2024       | 893777461466 | AWS Key Management Service                      |   26.57 |
| Nov 2024       | 893777461466 | AWS Lambda                                      |    0.00 |
| Nov 2024       | 893777461466 | AWS Secrets Manager                             |    0.84 |
| ........       | ............ | .......                                         |    .... |
| Nov 2024       | 893777461466 | CodeBuild                                       |    0.14 |
| Nov 2024       | 893777461466 | Tax                                             |   99.94 |
| Total Nov 2024 | 893777461466 | ALL SERVICES                                    |  879.67 |
+----------------+--------------+-------------------------------------------------+---------+
| Total          | 893777461466 | TOTAL ALL SERVICES PERIOD                       | 1936.91 |
+----------------+--------------+-------------------------------------------------+---------+
```

## Show Only Total Month by Range
You can to show only total month cost explorer report of date range

```bash
./aws-cost-explorer-report-cli.py -s 2024-10-01 -e 2024-11-30 --only-total --out csv 
+----------------+--------------+---------------------------+---------+
| Period         | Account      | Service                   |  Amount |
+----------------+--------------+---------------------------+---------+
| Total Oct 2024 | 893777461466 | ALL SERVICES              | 1057.24 |
+----------------+--------------+---------------------------+---------+
| Total Nov 2024 | 893777461466 | ALL SERVICES              |  879.67 |
+----------------+--------------+---------------------------+---------+
| Total          | 893777461466 | TOTAL ALL SERVICES PERIOD | 1936.91 |
+----------------+--------------+---------------------------+---------+
```
### CSV output file:
```csv
Period,Account,Service,Amount
Total Oct 2024,893777461466,ALL SERVICES,1057.24
Total Nov 2024,893777461466,ALL SERVICES,879.67
Total,893777461466,TOTAL ALL SERVICES PERIOD,1936.91
```

## Export results
Export the results types file as json, html, csv or text.

```bash
./aws-cost-explorer-report-cli.py -s 2024-05-01 -e 2024-11-30 --out csv

```


## Equivalent AWSCLI Command

Show cost report of date range [2024-10-01,2024-11-30]

```bash
$ aws --profile my-profile \
    ce get-cost-and-usage \
      --time-period "Start=2024-10-01,End=2024-11-30" \
      --granularity "MONTHLY" \
      --metrics "UnblendedCost" \
      --group-by "Type=DIMENSION,Key=LINKED_ACCOUNT" \
      --group-by "Type=DIMENSION,Key=SERVICE" \
      --output json
```

# License

[MIT LICENSE](LICENSE)

# References
[prettytable](https://github.com/prettytable/prettytable)

[boto3](https://github.com/boto/boto3)