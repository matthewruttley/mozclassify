# About
Algorithms for URL Classification. Will implement LICA, LWCA, LICA+DFR etc

# Usage

For LICA:

    >>> import classifier_LICA
    >>> classifier = classifier_LICA.LICA()
    >>> classifier.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
    [u'hobbies & interests', u'coins']

For LICA+DFR

    >>> import classifier_DFR
    >>> classifier = classifier_DFR.DFR()
    >>> classifier.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
    (u'hobbies & interests', u'coins')

# Performance

(Total documents tested: 1,000,001)

| Algorithm | Correct | Incorrect | Uncategorized | Precision | Recall |
|-----------|---------|-----------|---------------|-----------|--------|
| LICA      | 251,470 | 139,102   | 609,429       | 64.385    | 39.057 |
| DFR       | 373,158 | 401,885   | 224,958       | 48.147    | 77.504 |