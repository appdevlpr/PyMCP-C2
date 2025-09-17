#!/usr/bin/env python3

import argparse
import json
from datetime import datetime

def generate_report(input_file, report_type):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    if report_type == "executive":
        report = f"""
# Executive Penetration Test Report

## Overview
Date: {datetime.now().isoformat()}
Systems Tested: {len(data['agents'])}

## Key Findings
- Several critical vulnerabilities identified
- Unpatched systems found
- Weak authentication mechanisms

## Recommendations
- Apply security patches immediately
- Implement stronger authentication
- Enhance network segmentation
"""
    elif report_type == "technical":
        report = f"""
# Technical Penetration Test Report

## Details
Date: {datetime.now().isoformat()}

## Systems Tested
"""
        for agent in data['agents']:
            report += f"- {agent['hostname']} ({agent['ip_address']})\n"
        
        report += "\n## Findings\n"
        for agent in data['agents']:
            for result in agent['results']:
                report += f"### {agent['hostname']} - {result['command']}\n"
                report += f"Output: {result['output']}\n\n"
    
    return report

def main():
    parser = argparse.ArgumentParser(description='Generate penetration test report')
    parser.add_argument('--input', required=True, help='Input results file')
    parser.add_argument('--type', choices=['executive', 'technical'], default='executive', help='Report type')
    parser.add_argument('--output', help='Output file')
    args = parser.parse_args()
    
    report = generate_report(args.input, args.type)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

if __name__ == '__main__':
    main()
