from subprocess import call

if __name__ == "__main__":
    call("poetry run python runner.py", cwd="./scraper", shell=True)
