import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000
random.seed(None, version=2)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = dict()

    for page in corpus:
        chanceP = (1 - damping_factor) / len(corpus)

        if corpus[page]:
            if page in corpus[page]:
                chanceP += damping_factor / len(corpus)
            dist[page] = chanceP
 
    return dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageCounter = dict()
    pagerank = dict()
    


    currentpage = random.choice(list(corpus.keys()))
    print(currentpage)

    for page in corpus:
        pageCounter[page] = 0

    for i in range(1, n):
        pageCounter[currentpage] += 1
        currentpage = random.choice(list(transition_model(corpus, currentpage, damping_factor)))

    for page in pageCounter:
        pagerank[page] = pageCounter[page] / n


    return pagerank


def iterate_pagerank(corpus, damping_factor):             
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    end = False
    while (not(end)):
        nextrank = dict()

        for page in corpus:
            end = True
            nextrank[page] = (1 - damping_factor) / len(corpus)

            for key, links in corpus.items():
                if links:
                    if key != page and page in links:
                        nextrank[page] += damping_factor * (pagerank[key] / len(corpus[key]))
                else:
                    nextrank[page] += damping_factor * (pagerank[key] / len(corpus))
            if round(nextrank[page]-pagerank[page], 3) == 0:
                end = False
            
        if not(end):
            return nextrank
        pagerank = nextrank.copy()
    return pagerank



if __name__ == "__main__":
    main()
