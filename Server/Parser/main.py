from config import RESOURCES
from parsers.cybernews import CyberNewsParser
from dotenv import load_dotenv
from multiprocessing import Process, Semaphore

def process_category(category, link, semaphore):
    with semaphore:
        cybernews_parser = CyberNewsParser(url=link)
        cybernews_parser.start()

def main():
    semaphore = Semaphore(2)  # Set the maximum number of allowed processes to 1
    processes = []
    for category, link in RESOURCES["cybernews"].items():
        p = Process(target=process_category, args=(category, link, semaphore))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()

if __name__ == "__main__":
    load_dotenv()
    main()
