from multiprocessing import get_all_start_methods
import os
import requests


def get_company_facts(cik: int) -> dict:
    """ Retrieve company facts from the SEC EDGAR."""
    url = (
        "https://data.sec.gov/api/xbrl/"
        f"companyfacts/CIK{cik:010d}.json"
    )

    headers = {
"User-Agent": os.environ["SEC_USER_AGENT"],
"Accept-Encoding": "gzip, deflate",

    }

    response = requests.get(url, 
    headers=headers,
    timeout=30,
    )

    response.raise_for_status()

    return response.json()


    if __name__ == "__main__":

        alphabet == get_company_facts(1652044)

        print(alphabet["entityName"])
        print(alphabet["cik"])

        