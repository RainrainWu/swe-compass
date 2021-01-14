import json
import argparse
from subprocess import call

from analyzer.planner import Planner
from config import PlannerConfig

parser = argparse.ArgumentParser()
parser.add_argument(
    "--update",
    "-u",
    action="store_true",
    help="update job description samples by scrapers",
    default=False,
)
args = parser.parse_args()


if __name__ == "__main__":
    if args.update:
        call("poetry run python runner.py", cwd="./scraper", shell=True)
    else:
        planner = Planner(PlannerConfig.run_plan)
        planner.run()
