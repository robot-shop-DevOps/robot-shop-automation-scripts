import argparse
from datetime import datetime

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="azure",
            description="Azure Automation CLI Tool"
        )

        self.resource_parser = self.parser.add_subparsers(
            dest="resource",
            required=True
        )

        self.acrParser()


    def acrParser(self):
        acr = self.resource_parser.add_parser(
            "acr",
            help="Azure Container Registry operations"
        )

        acr.add_argument(
            "--acr-endpoint",
            required=True,
            help="ACR endpoint"
        )

        acr_sub = acr.add_subparsers(dest="command", required=True)

        p = acr_sub.add_parser("cleanup-tags", help="Delete tags between dates")
        p.add_argument("--repo", required=True)
        p.add_argument(
            "--start-date", 
            required=True, 
            type=self.parse_date, 
            help="Start date in YYYY-MM-DD format"
        )
        p.add_argument(
            "--end-date", 
            required=True, 
            type=self.parse_date, 
            help="End date in YYYY-MM-DD format"
        )
        p.add_argument("--log-level", 
            required=False, 
            default="INFO", 
            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            help="Logging level of the application"
        )

        p = acr_sub.add_parser(
            "cleanup-manifests", 
            help="Delete manifests between dates"
        )
        p.add_argument(
            "--start-date", 
            required=True, 
            type=self.parse_date, 
            help="Start date in YYYY-MM-DD format"
        )
        p.add_argument(
            "--end-date", 
            required=True, 
            type=self.parse_date, 
            help="End date in YYYY-MM-DD format"
        )

    
    def parse_date(self, value: str):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid date format: '{value}'. Use YYYY-MM-DD"
            )
        
        
    def parse(self):
        return self.parser.parse_args()