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
2019/03/22 (Simon) - added active page indication
2019/03/26 (Simon) - changed page arguments, updated UI
2019/03/27 (Simon) - slightly updated UI
</%doc>


<%doc>
    (string) current
    (tuple) user ((string) ID, (int) Type)
</%doc>
<%page args="user=None, current=None"/>


<%
from collections import defaultdict
is_active = defaultdict(lambda:"")
is_active[current] = "active"
if user is None:
    user = (None, -1)
ID, type = user
%>

<div class="ui container">
    <div class="ui hidden fitted horizontal divider"></div>
    <h1 class="ui image header">
        <img src="/static/psysc.png" class="ui image" style="margin:0">
        <div class="content">
            <a href="/">PSYSC</a>
            <div class="tiny sub header">Affiliation Database</div>
        </div>
    </h1>
</div>
<div class="ui fluid container">
    <div class="ui stackable secondary inverted blue menu" style="margin:0 0 2rem 0">
        <div class="ui container">
            <a class="${is_active['index']} item" href="/index">Home</a>
            % if type == -1:
            <a class="${is_active['apply']} item" href="/apply">Application form</a>
            % elif type == 0:
            <a class="${is_active['view']} item" href="/view">View record</a>
            <a class="${is_active['apply']} item" href="/apply">Apply for renewal</a>
            % elif type == 1:
            <a class="${is_active['applications']} item" href="/applications">Pending applications</a>
            <a class="${is_active['add']} item" href="/add">Add record</a>
            <a class="${is_active['view']} item" href="/view">View records</a>
            <a class="${is_active['summary']} item" href="/summary">Summary</a>
            % else:
            <a class="${is_active['add']} item" href="/add">AddRecord</a>
            <a class="${is_active['view']} item" href="/view">ViewRecord</a>
            <a class="${is_active['apply']} item" href="/apply">AddApplication</a>
            <a class="${is_active['applications']} item" href="/applications">ViewApplication</a>
            <a class="${is_active['summary']} item" href="/summary">Summary</a>
            % endif
            <div class="right menu">
                % if ID is not None:
                <i class="ui item">
                    % if type is not 2:
                    <b>${ID}</b>
                    % else:
                    <i class="inverted small red circular bug icon"></i><b>${ID}</b>
                    % endif
                </i>
                % endif
                % if type == -1:
                <a href="/login" class="ui item"><b>Sign in</b></a>
                % else:
                <a href="/logout" class="ui item"><b>Sign out</b></a>
                % endif
                </div>
        </div>
    </div>
</div>
