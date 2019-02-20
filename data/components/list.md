<!--  This intent is for listing the resources found in a page -->
## intent:list_resources
- list me [proposals](resource)
- list [recipes](resource)
- can you list me [articles](resource)
- make a list of [songs](resource)
- show me a list of [cities](resource)
- read a list of [recipes](resource)
- enumerate a list of [proposals](resource)
- read me please the list of [movies](resource)
- could you tell me the list of [flights](resource)
- please list the [papers](resource)
- what are the [news](resource)
- read [cards](resource)

<!-- This intent is for providing statistics about a list -->
## intent:list_count
- how many [resources](resource)
- tell me how many [resources](resource) there are
- how many are there?
- what's the number of [elements](resource)
- could you tell me how many [bookings](resource)
- what's the total number of [results](resource)
- could you tell me how many?
- please tell me how many [bikes](resource)

<!--  This intent is for filtering the elements of the list -->
## intent:list_filter
- leave out [people](resource) with [name](attribute) [carlos](attr-value)
- filter out [cars](resource) with [price](attribute) [greater than](filter_op:greater) [1000](attr-value)
- filter out [comedy](attr-value) [events](resource)
- omit [tickets](resource) with [price](attribute) [less than](filter_op:less) [1000](attr-value)
- exclude [products](resource) that are [not](filter_op:different) [books](attr-value)
- show me only those [comedy](attr-value) [events](resource)
- show me those with [price](attribute) [greater than](filter_op:greater) [1000](attr-value)
- read those with [price](attribute) [greater than](filter_op:greater) than [1000](attr-value)
- list [users](resource) with [name](attribute) [matrix](attr-value)
- list those with [name](attribute) [equals to](filter_op:equals) [matrix](attr-value)
- plase list [videos](resource) with [more than](filter_op:greater) [10](attr-value) [views](attribute)


<!--  This intent is for selecting the attributes of a resource to be listed -->
## intent:list_summary
- list the [countries](resource) [only](summary_op) by [capital](attribute)
- read [only](summary_op) [name](attribute) and [date](attribute)
- read [also](summary_op:add) the [price](attribute)
- read [all](summary_op) the information
- [don't tell](summary_op:remove) me the [cost](attribute)
- [exclude](summary_op:remove) the [description](attribute)
- read [all](summary_op) [except](summary_op:remove) reviews
- please read [also](summary_op:add) the [destination](attribute)
- please show [as well](summary_op:add) [departure time](attribute) and [arrival time](attribute)

<!--  This intent is for loading more resources -->
## intent:list_more
- Are there any more [resources](resource)
- list more [toys](resource) 
- continue listing [dresses](resource) 
- more [glasses](resource) please
- please go on with the [papers](resource) 
- continue with the list
- more [pictures](resource) 
- keep going

<!--  This intent is for changing the order of the list -->
## intent:list_sort
- sort [boxes](resource) by [weight](attribute)
- sort the list by [length](attribute)
- read [boxes](resource) starting from the [highest](sort_op:descending) [length](attribute)
- could you list [cups](resource) starting from the [smallest](sort_op:ascending) [size](attribute)
- list [bottles](resource) in [descending](sort_op) order
- [toys](resource) sorted by [year](attribute)
- read [dolls](resource) ordered by [color](attribute)
- enumerate it in [descending](sort_op) order
- list [boats](resource) by [owner](attribute) in [ascending](sort_op) order
- read by [ranking](attribute) in [descending](sort_op) order
- read the list in [ascending](sort_op) order
- start from the [last](sort_op:reverse)
- begin from the [first](sort_op:noop)
- please start from the [end](sort_op:reverse)
- begin from the [beginning](sort_op:noop)

<!--   This intent is for navigating the elements of the list -->
## intent:list_navigate
- go to [previous](nav_op)
- go to the [one before](nav_op:previous)
- read [next](nav_op)
- read the [one after](nav_ope:next)
- can you [repeat](nav_op) please?
- go to the [first](nav_op) [article](resource)
- go to the [second](nav_op)
- read the [third](nav_op) one
- read the [fourth](nav_op) element


<!-- This intent is for asking information (attributes) about the resource -->
## intent:list_about
- what information do we have about [emails](resource)
- details about [planes](resource)
- what can you tell me about [books](resource)
- tell me about [books](resource)
- information about [novels](resource)
- properties of [women](resource)
- attributes of [babies](resource)
- what is a [sound](resource)
- what about [lights](resource)


## lookup:sort_op
- descending
- ascending
- reverse
- noop

## lookup:filter_op
- equals
- greater 
- less 
- different

## lookup:summary_op
- only
- add
- remove
- all

## synonym:descending
- highest
- highest first
- top down
- biggest

## synonym:ascending
- lowest
- smallest
- bottom up
- smallest first

## synonym:greater
- greater than
- more than
- after 

## synonym:less
- less than
- fewer than
- before

## synonym:equals
- equals to
- same as

## synonym:different
- different from
- not equal to


## regex:resource
- [^\s]*s

