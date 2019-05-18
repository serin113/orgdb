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
2019/03/29 (Simon) - home and login/logout icons added
2019/04/02 (Simon) - added /dialog for debugging (dev accounts only)
2019/04/24 (Simon) - updated username field format
2019/05/17 (Simon) - removed inline styles
2019/05/18 (Simon) - added menu icons
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
        <img src="/static/psysc.png" class="ui image" id="logo">
        <div class="content">
            <a href="/">PSYSC</a>
            <div class="tiny sub header">Affiliation Database</div>
        </div>
    </h1>
</div>
<div class="ui fluid container">
    <div class="ui stackable secondary inverted blue menu" id="menu">
        <div class="ui container">
            <a class="${is_active['index']} item" href="/index"><i class="home icon"></i> Home</a>
            % if type == -1:
            <a class="${is_active['apply']} item" href="/apply"><i class="users icon"></i> Application form</a>
            % elif type == 0:
            <a class="${is_active['view']} item" href="/view"><i class="database icon"></i> View record</a>
            <a class="${is_active['apply']} item" href="/apply"><i class="users icon"></i> Apply for renewal</a>
            % elif type == 1:
            <a class="${is_active['applications']} item" href="/applications"><i class="clipboard check icon"></i> Pending applications</a>
            <a class="${is_active['add']} item" href="/add"><i class="plus circle icon"></i> Add record</a>
            <a class="${is_active['view']} item" href="/view"><i class="database icon"></i> View records</a>
            <a class="${is_active['summary']} item" href="/summary"><i class="file icon"></i> Summary</a>
            % elif type == 2:
            <a class="${is_active['add']} item" href="/add"><i class="plus circle icon"></i> AddRecord</a>
            <a class="${is_active['view']} item" href="/view"><i class="database icon"></i> ViewRecord</a>
            <a class="${is_active['apply']} item" href="/apply"><i class="users icon"></i> AddApplication</a>
            <a class="${is_active['applications']} item" href="/applications"><i class="clipboard check icon"></i> ViewApplication</a>
            <a class="${is_active['summary']} item" href="/summary"><i class="file icon"></i> Summary</a>
            <a class="item" href="/dialog">Dialog</a>
            % endif
            <div class="right menu">
                % if ID is not None:
                <i class="ui item">
                    % if type is not 2:
                    <i class="user circle icon"></i>
                    % else:
                    <i class="inverted small red circular bug icon"></i>
                    % endif
                    <b>${ID}</b>
                </i>
                % endif
                % if type == -1:
                <a href="/login" class="ui item"><i class="sign-in icon"></i> Login</a>
                % else:
                <a href="/logout" class="ui item"><i class="sign-out icon"></i> Logout</a>
                % endif
                </div>
        </div>
    </div>
</div>
