#
# Title: main.py
# Authors: Sofiia Khutorna, Rem D'Ambrosio
# Created: 2024-09-20
#

import argparse
from Puller import Puller   
from Builder import Builder
from Checker import Checker
from Reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description='analyzes devices to predict site health')
    parser.add_argument('-pu', '--pull', action='store_true', help='pull new data from APIs')
    parser.add_argument('-bu', '--build', action='store_true', help='build device objects from raw data')
    parser.add_argument('-ch', '--check', action='store_true', help='check health of devices')
    parser.add_argument('-re', '--report', action='store_true', help='output report')
    parser.add_argument('-pa', '--path', type=str, help='path for input/output data', default='/anon/path')
    args = parser.parse_args()
    path = args.path

    if args.pull:
        pull(path)
    
    if args.build:
        build(path)
    
    if args.check:
        check(path)

    if args.report:
        report(path)

    return

 
def pull(path):
    print("Pulling data from all sources...")
    puller = Puller(path)
    puller.pull_api_data(5)
    print("...Done pulling data.")
    return


def build(path):
    print("Building sites and devices...")
    builder = Builder(path)
    builder.create_site_folders()
    print("...Created site folders...")
    builder.build_routers()
    print("...Built routers...")
    builder.build_switches()
    print("...Built switches...")
    builder.build_aps()
    print("...Built APs...")
    builder.build_modems()
    print("...Built modems...")
    builder.build_seleneboxes()
    print("...Built seleneboxes...")
    builder.save_range()
    print("...Saved range to file...")
    print("...Done building sites and devices.")
    return


def check(path):
    print("Checking health of sites...")
    checker = Checker(path)
    sites = checker.build_sites()
    print("...Determined health scores...")
    checker.to_json(sites)
    print("...Saved site health scores to file.")
    return


def report(path):
    print("Generating report...")
    reporter = Reporter(path)
    report = reporter.create_report()
    print("...Created report...")
    reporter.to_csv(report)
    print("...Saved report to file.")
    return


if __name__ == '__main__':
    main()
