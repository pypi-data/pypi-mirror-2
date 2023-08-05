""" Source Lines of Code (SLOC)
    This type of metric counts the lines but excludes empty lines and comments.
    In literature this is also referred as physical lines of code.

"""
__author__ = 'Mark Fink <mark@mark-fink.de>'

from metricbase import MetricBase

token_types = [
    b'Keyword',
    b'Name',
    b'Punctuation',
    b'Operator',
    b'Literal']


class SLOCMetric(MetricBase):
    """ Compute the SLOC Metric for the whole source file."""

    def __init__(self, context):
        self.context = context
        self.reset()
    
    def reset(self):
        """Reset metric counter."""
        self.metrics = {'sloc': 0, 'comments': 0}
        self.contains_code = False # does the current line contain code

    def process_token(self, tok):
        """count comments and non-empty lines that contain code"""
        #print tok
        if(tok[0].__str__() in ('Token.Comment.Multiline', 'Token.Comment', 
                'Token.Literal.String.Doc')):
            self.metrics['comments'] += tok[1].count('\n')+1            
        elif(tok[0].__str__() in ('Token.Comment.Single')):
            self.metrics['comments'] += 1            
        elif(self.contains_code and tok[0].__str__().startswith('Token.Text') and
                tok[1].count(u'\n')):
            # start new line
            self.contains_code = False
            self.metrics['sloc'] += 1
        # for c style includes
        elif(tok[0].__str__() == 'Token.Comment.Preproc' and 
                tok[1].count(u'\n')):
            # start new line
            self.contains_code = False
            self.metrics['sloc'] += 1
        elif(tok[0][0] in token_types):
            self.contains_code = True

    def display_header(self):
        """ Display header for SLOC metric"""
        print '%30s %11s %7s' % ('Language', 'SLOC', 'Comment'),

    def display_separator(self):
        """ Display separator for SLOC metric"""
        print '%s %s %s' % ('-'*30, '-'*11, '-'*7),

    def display_metrics(self, metrics):
        """ Display Source Lines of Code metric (SLOC) """
        print '%30s %11d %7d' % (metrics['language'], metrics['sloc'], \
            metrics['comments']),
