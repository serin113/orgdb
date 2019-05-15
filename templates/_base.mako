<%doc>
Created in 2019-05-11 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/05/11 (Simon) - added initial template with filters
</%doc>

<%
import re
def remove_whitespace(stri):
    #stri = re.sub(r"<!--(?:.|\s)*?-->", "", stri, 0, re.MULTILINE)
    stri = re.sub(r"\s\s*", " ", stri, 0, re.MULTILINE)
    stri = re.sub(r">(?:\s*)<", "><", stri, 0, re.MULTILINE)
    return stri
%>

${capture(self.body, **context.kwargs) | remove_whitespace}