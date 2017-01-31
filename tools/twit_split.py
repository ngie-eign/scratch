#!/usr/bin/env python
"""For splitting up long messages into something that Twitter can digest
and with clean pagination formatting, if requested.
"""

import argparse
import re
import sys

# Q: Why always "23"?
# A: https://support.twitter.com/articles/78124
URL_SHORTENED_LEN = 23

# You really should write a blog post instead. Twitter's the wrong medium
MAX_POSTS = 100

# => len(' ')
SPACE_LEN = 1

# https://support.twitter.com/articles/101299#error
#
# I realize the character set is \w, but I'm trying to avoid unnecessary
# `os.environ` munging since twitter doesn't support unicode chars for
# usernames and LOCALE/UNICODE messes with \w behavior wise.
TWITTER_USERNAME_RE = '^[a-zA-Z0-9_]+$'

# Q: Why 140?
# A: It's built into the API (seriously though..):
#    https://dev.twitter.com/basics/counting-characters
TWITTER_MAX_POST_LEN = 140


class RecipientsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not re.match(TWITTER_USERNAME_RE, values):
            raise ValueError('Recipients must match the following regex: %s' %
                             (TWITTER_USERNAME_RE))
        recipients = getattr(namespace, self.dest)
        recipients.append(values)


def main():
    """And then, there was main.."""

    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=sys.stdin)
    ap.add_argument('--omit-pagination', action='store_true', default=False)
    ap.add_argument('recipients', action=RecipientsAction, default=[])
    args = ap.parse_args()

    recipient_prefix = ' '.join(['@%s' % (r) for r in args.recipients])

    # Need to read in the entire message first to get an accurate count for the
    # space needed for pagination
    if args.input == sys.stdin:
        overall_message_by_line = sys.stdin.readlines()
        sys.stdin.close()
    else:
        with open(args.input) as fp:
            overall_message_by_line = fp.readlines()

    if args.omit_pagination:
        pagination_reserved_amount = 0
    else:
        # XXX: 2 chars worth of slop included with single-digit posts
        pagination_reserved_amount = len("xx/yy")

    prefix_reserved_len = len(recipient_prefix) + pagination_reserved_amount

    reformatted_lines = []

    # Need to split up message by lines, count characters in words, then split
    # by word, paying attention to avoiding overflow per line or splitting up
    # words per line.
    for line in overall_message_by_line:
        line = line.rstrip()
        while line:

            reformatted_line_max_len = \
                TWITTER_MAX_POST_LEN - prefix_reserved_len
            if len(line) <= reformatted_line_max_len:
                reformatted_lines.append(line)
                break

            last_word_index = 0
            new_found_index = -1

            while True:
                new_found_index = line.find(' ', last_word_index + 1,
                                            reformatted_line_max_len)
                if (new_found_index == -1 or
                    last_word_index == new_found_index):
                    break
                last_word_index = new_found_index

            reformatted_line = line[:last_word_index].rstrip()
            reformatted_lines.append(reformatted_line)
            line = line[len(reformatted_line):].lstrip()

    num_posts = len(reformatted_lines)
    if num_posts > MAX_POSTS:
        sys.exit('Number of posts is waaay too much (>%d); post the content '
                 'to a blog instead and summarize it on Twitter' % (num_posts))
    prefix_format_str = \
        ' %(fqs)s/%(fqs)s' % {'fqs' : '%%%dd' % (len(str(num_posts)))}
    for i, reformatted_line in enumerate(reformatted_lines, 1):
        prefix = recipient_prefix
        if pagination_reserved_amount:
            prefix += prefix_format_str % (i, num_posts)
        print('%s %s' % (prefix, reformatted_line))


if __name__ == '__main__':
    main()
