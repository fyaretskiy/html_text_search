website_parse module has query method:
query("query", "url") checks if "query" is present in url HTML text (extracted by BeautifulSoup)
query string takes simple, or complex boolean form.
simple boolean form examples: "apple", "NOT apple", "apple OR NOT cherries", "any AND combination AND of AND statements"
simple boolean strings become list of Item objects where Item.name is the identifier and Item.sign describes if the element should be negated.
The list of Item objects then becomes a list of booleans
Complex boolean expressions are put into a parse tree where the nodes are Item objects. The tree is then traversed in a
post order way to change the nodes into booleans.


simple query example: build_list("apples AND fish AND NOT bagels", "fish bagels apples")
"apples AND fish AND NOT bagels" -> [Item, Item, Item]
first Item: Item.name = "apples", Item.sign = None
third Item: Item.name = "fish", Item.sign = None
fifth Item: Item.name = "bagels", Item.sign = "NOT"
-> [True, True, False] -> False

complex query example: build_tree("( NOT ( ( stacy AND adam )  OR betty ) AND frank )", "adam betty frank")
"( NOT ( ( stacy AND adam )  OR betty ) AND frank )"

                                    Item1
                Item2                                      Item3
    Item4                   Item5
Item6  Item7
###################################################################### ->
                                    AND
                OR (NOT)                           frank
        AND            betty
   stacy     adam

Item1.name = AND, Item1.sign = None
Item2.name = OR, Item2.sign = NOT, Item3.name = frank, Item3.sign = NONE
Item4.name = AND, Item4.sign = NONE, Item5.name = betty, Item5.sign = NONE
Item6.name = stacy, Item6.sign = NONE, Item7.name = adam, Item7.sign = NONE

Post Order Evaluation:
First iteration:

             AND
      OR               frank
False   betty

Second iteration:

            AND
      False      frank

Third iteration:

            False



