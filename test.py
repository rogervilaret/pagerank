from pagerank import DAMPING, SAMPLES, sample_pagerank



corpus1 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

corpus2 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html", "1.html"}, "3.html": {"2.html","4.html"}, "4.html":{"1.html"}}

print(sample_pagerank(corpus2,DAMPING,SAMPLES))