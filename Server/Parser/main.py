from config import SOURCES
from parsers.cybernews import CyberNewsParser
from dotenv import load_dotenv
from multiprocessing import Process, Semaphore

def process_category(link, semaphore):
    with semaphore:
        cybernews_parser = CyberNewsParser(url=link)
        cybernews_parser.start()

def main():
    semaphore = Semaphore(2)  # Set the maximum number of allowed processes to 1
    processes = []
    for source in SOURCES:
        for link in source["urls"]:
            p = Process(target=process_category, args=(link, semaphore))
            p.start()
            processes.append(p)
        
        for p in processes:
            p.join()

if __name__ == "__main__":
    load_dotenv()
    main()
