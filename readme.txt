website_parse module has query method:
query("query", "url") checks if "query" is present in url HTML text (extracted by BeautifulSoup)
query string takes simple, or complex boolean form.
simple boolean form examples: "apple", "NOT apple", "apple OR NOT cherries", "any AND combination AND of AND statements"
simple boolean strings create list of Item objects that contain the word or operator (OR, AND) and presence of preceding NOT
The list of Item objects then becomes a list of booleans
Complex boolean expressions are put into a parse tree where the nodes are Item objects. The tree is then traversed in a
post order form to change the nodes into booleans.
