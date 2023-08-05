# CSSPrefixer
# Copyright 2010 MyFreeWeb <me@myfreeweb.ru>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cssutils

from rules import rules as tr_rules

def process(string, debug=False, minify=False):
    if debug:
        loglevel = 'info'
    else:
        loglevel = 'error'
    parser = cssutils.CSSParser(loglevel=loglevel)
    if minify:
        cssutils.ser.prefs.useMinified()
    sheet = parser.parseString(string)
    result = ''
    for ruleset in sheet.cssRules:
        if hasattr(ruleset, 'style'): # Comments doesn't
            for rule in ruleset.style.children():
                try:
                    processor = tr_rules[rule.name](rule)
                    [ruleset.style.setProperty(prop) for prop in processor.get_prefixed_props()]
                    result += processor.pure_css_hook()
                except: # Comments, etc.
                    if debug:
                        print 'warning with ' + str(rule)
            result += unicode(ruleset.cssText)

    # Not using sheet.cssText - it's buggy:
    # it skips some prefixed properties.
    return result

__all__ = ('process')
