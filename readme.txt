website_parse module has query method:
query("query", "url") checks if "query" is present in url HTML text (extracted by BeautifulSoup)
query string takes simple, or complex boolean form.
simple boolean form examples: "apple", "NOT apple", "apple OR NOT cherries", "any AND combination AND of AND statements"
simple boolean strings become list of Item objects where Item.name is the identifier and Item.sign describes if the element should be negated.
The list of Item objects then becomes a list of booleans
Complex boolean expressions are put into a parse tree where the nodes are Item objects. The tree is then traversed in a
post order way to change the nodes into booleans.
