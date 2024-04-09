from multiprocessing import Process, Semaphore


from parsers.cybernews import CyberNewsParser
from config import SOURCES

def process_category(link, language_code, semaphore):
    with semaphore:
        cybernews_parser = CyberNewsParser(url=link, language_code=language_code)
        cybernews_parser.start()

def main():
    semaphore = Semaphore(2)  # Set the maximum number of allowed processes to 1
    processes = []
    for source in SOURCES:
        for link in source["urls"]:
            p = Process(target=process_category, args=(link, source["language_code"], semaphore))
            p.start()
            processes.append(p)
        
        for p in processes:
            p.join()

if __name__ == "__main__":
    main()
