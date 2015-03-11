# About
Algorithms for URL Classification. Will implement LICA, LWCA, DFR etc

# Usage

For LICA:

    >>> import classifier_LICA
    >>> classifier = classifier_LICA.LICA()
    >>> classifier.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
    [u'hobbies & interests', u'coins']

For DFR

    >>> import classifier_DFR
    >>> classifier = classifier_DFR.DFR()
    >>> classifier.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
    (u'hobbies & interests', u'coins')
	
To use the title and url for either algorithm, use a named argument like: `classifier.classify("http://domain.com", title="Interesting Coin Website")`

# Performance

(Total documents tested: 1,000,001)

| Algo           |  Dataset  | Level   | Correct | Incorr. | Unknown | Prec.  | Recall |
|----------------|-----------|---------|---------|---------|---------|--------|--------|
| LICA           | URLs only | Top+Sub | 251,470 | 139,102 | 609,429 | 64.385 | 39.057 |
| LICA           | URLs only | Top     |         |         |         |        |        |
| LICA           | URL+title | Top+Sub |         |         |         |        |        |
| LICA           | URL+title | Top     |         |         |         |        |        |
| DFR            | URLs only | Top+Sub | 373,158 | 401,885 | 224,958 | 48.147 | 77.504 |
| DFR            | URLs only | Top     |         |         |         |        |        |
| DFR            | URL+title | Top+Sub | 467,160 | 354,201 | 178,640 | 56.876 | 82.136 |
| DFR            | URL+title | Top     |         |         |         |        |        |
| DFR rules only | URLs only | Top+Sub | 337,687 | 423,260 | 239,054 | 44.377 | 76.095 |
| DFR rules only | URLs only | Top     |         |         |         |        |        |
| DFR rules only | URL+title | Top+Sub | 337,687 | 423,260 | 239,054 | 44.377 | 76.095 |
| DFR rules only | URL+title | Top     |         |         |         |        |        |
