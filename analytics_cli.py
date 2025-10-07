import argparse
from analytics import sales_by_day, revenue_period, top_customers

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("daily")
    p1.add_argument("--days", type=int, default=7)

    p2 = sub.add_parser("period")
    p2.add_argument("--start", required=True)
    p2.add_argument("--end", required=True)

    p3 = sub.add_parser("top")
    p3.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()
    if args.cmd == "daily":
        sales_by_day(args.days)
    elif args.cmd == "period":
        revenue_period(args.start, args.end)
    elif args.cmd == "top":
        top_customers(args.limit)

if __name__ == "__main__":
    main()
