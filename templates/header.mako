<%doc>
Created in 2019-02-13 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/13 (Simon) - added initial template
2019/02/15 (Simon) - added basic navbar
2019/03/07 (Simon) - added /apply link
2019/03/12 (Simon) - added /applications link
2019/03/21 (Simon) - added /summary link
</%doc>

<%page args="current=None"/>

<h1 class="center"><a href="/">PSYSC</a></h1>

<%
from collections import defaultdict
is_active = defaultdict(lambda:"")
is_active[current] = "active"
%>

<div class="ui six item menu">
    <a class="${is_active['index']} item" href="/index">Home</a>
    <a class="${is_active['add']} item" href="/add">Add Record</a>
    <a class="${is_active['view']} item" href="/view">View Records</a>
    <a class="${is_active['apply']} item" href="/apply">Create Application</a>
    <a class="${is_active['applications']} item" href="/applications">View Applications</a>
    <a class="${is_active['summary']} item" href="/summary">View Summary</a>
</div>
