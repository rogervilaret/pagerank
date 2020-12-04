import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    #first function
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages_num = len(corpus.keys())
    total_links = 0
    link_pages = set()
    
    #looking for the lins that are going
    for link in corpus[page]:
        total_links = total_links + 1
        link_pages.add(link)

    pages_probability = {}
    
    
    #if not links the damping factor disapear
    casual_damping = damping_factor
    
    if len(link_pages) == 0:
        casual_damping= 0

    for each_page in corpus:
        probability = 0
        if each_page in link_pages:
            probability = damping_factor / total_links
        
        #adding damping_factor probability
        probability = round(probability + (1 - casual_damping) / pages_num, 5)
        pages_probability.update({ each_page : probability })
    
    return pages_probability
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #load dictionay transition model 
    dict_transitions= {} 
    distributions = {}
    for each_page in corpus:
        dict_transitions.update({each_page : transition_model(corpus, each_page, damping_factor)})
        distributions.update({each_page : 0})

    
    #random first page
    working_page = random.choice( list(dict_transitions.keys()))

    

    #sample starts
    
    for i in range(0, n):
        distributions.update({working_page : (distributions.get(working_page) + 1)})
        # take next probability
        next_probabilities = dict_transitions.get(working_page)

        # random jump to next page
        randnum = random.random()

        acumulate = 0
        for next_page in next_probabilities:
            acumulate = acumulate + next_probabilities.get(next_page)
            if acumulate > randnum:
                working_page = next_page
                break
            
      
    # Format return dictionary
    probabilities = {}
    for each_page in distributions:
        probabilities.update({ each_page : (distributions.get(each_page) / n) })

    return probabilities

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Inizialize the pageranks
    probabilities = {}
    for each_page in corpus:
        probabilities.update({ each_page : (1 / len(corpus.keys())) })
    
    
    while True:
        check_end = 0
        for key1 in corpus:
            previous_probability = probabilities.get(key1)
            
            #recalculate probability
            #not damping side
            probability1 = (1 - damping_factor) / len(corpus.keys())
            
            probability2 = 0
            for keylink in corpus:
                #check if there are some link
                if len(corpus.get(keylink)) > 0:
                    if key1 in corpus.get(keylink):
                        probability2 = probability2 + ( probabilities.get(keylink) / len(corpus.get(keylink)))
                        
                #page without links
                else:
                    alllinks = corpus.keys()
                    probability2 = probability2 + ( probabilities.get(keylink) / len(alllinks))

            
            probability = probability1 + (probability2 * damping_factor)

            probabilities.update({key1 : probability})

            if abs(probability - previous_probability) < 0.0001:
                check_end = check_end + 1
            
        if check_end == len(corpus.keys()):
            break
       

    return probabilities
    raise NotImplementedError


if __name__ == "__main__":
    main()
