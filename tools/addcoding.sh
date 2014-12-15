# -*- coding: utf-8 -*-
#!/bin/bash
for file in "$@"; do
    ed $file <<EOF
1
i
# -*- coding: utf-8 -*-
.
w
q
EOF
    done
