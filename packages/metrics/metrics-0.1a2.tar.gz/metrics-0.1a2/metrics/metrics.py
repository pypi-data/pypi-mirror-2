#! /usr/bin/env python
""" metrics package for source code.

    Orignally based on grop.py by Jurgen Hermann.
    PyMetrics by Reg. Charney to do Python complexity measurements.
    Simplified and reduced functionality by Mark Fink

    Copyright (c) 2001 by Jurgen Hermann <jh@web.de>
    Copyright (c) 2007 by Reg. Charney <charney@charneyday.com>
    Copyright (c) 2010 by Mark Fink <mark@mark-fink.de>

    All rights reserved, see LICENSE for details.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""
__author__ = 'Mark Fink <mark@mark-fink.de>'

import sys
from pygments.lexers import guess_lexer_for_filename
from processargs import ProcessArgs, ProcessArgsError
from compute import ComputeMetrics

PYTHON_VERSION = sys.version[:3]


def __import_metric_modules(include_metrics):
    """ Import the modules specified in the parameter list.

    includeMetrics is a list of (metricModuleName, metricClassName)
    pairs. This function defines a dictionary containing only valid
    module/class names. When an error is found, the invalid
    module/class pair is removed from the included list of metrics.
    """
    i = 0
    metric_modules = {}
    if PYTHON_VERSION < '2.5':
        pfx = '' # this fix is for Python 2.4
    else:
        pfx = 'metrics.'
    for m, n in include_metrics:
        try:
            mm = pfx + m
            if PYTHON_VERSION < '2.5':
                mod = __import__(mm, globals(), locals(), [m])
            else:
                mod = __import__(mm, fromlist=[m])
            metric_modules[m] = mod
            i += 1
        except ImportError:
            sys.stderr.write(
                "Unable to import metric module %s -- ignored.\n\n" % mm)
            # remove the erroneous metric module/class tuple
            del include_metrics[i]

    return metric_modules


def __instantiate_metric(metric_modules, context):
    """ Instantiate all user specified metric classes.

    The code works by finding the desired metric class in a metric module and
    instantiating the class. It does this by assuming that the metric
    class is in the dictionary of the metric module.
    """
    metric_instance = {}
    inclIndx = -1
    for m, n in context['include_metrics']:
        inclIndx += 1
        try:
            metric_instance[m] = None # default if metric class does not exist.
            metric_instance[m] = metric_modules[m].__dict__[n](context)
        except KeyError:
            sys.stderr.write('Module %s does not contain metric class %s' + \
                ' -- metric %s ignored.\n\n' % (m, n, m))
            del(metric_instance[m])
            del(context['include_metrics'][inclIndx])

    return metric_instance


def display_header(context, metric_instance, before='', after=''):
    """Display the header for the summary results."""
    print before,
    for m, n in context['include_metrics']: # display in the order of apperance
        metric_instance[m].display_header()
    print after


def display_separator(context, metric_instance, before='', after=''):
    """Display the header for the summary results."""
    print before,
    for m, n in context['include_metrics']:
        metric_instance[m].display_separator()
    print after


def display_metrics(context, metric_instance, before='', after='', metrics=[]):
    """Display the header for the summary results."""
    print before,
    for m, n in context['include_metrics']:
        metric_instance[m].display_metrics(metrics)
    print after


def main():
    try:
        pa = ProcessArgs()
        context = {}
        context['in_file_names'] = pa.in_file_names
        context['include_metrics'] = pa.include_metrics
        context['quiet'] = pa.quiet
        context['verbose'] = pa.verbose
        process(context)
    except ProcessArgsError, e:
        sys.stderr.writelines(str(e))
    sys.exit(0)


def process(context):
    """ Main routine for PyMetrics."""
    metrics = {}
    # import all the needed metric modules
    metric_modules = __import_metric_modules(context['include_metrics'])

    # instantiate all the desired metric classes
    metric_instance = __instantiate_metric(metric_modules, context)

    cm = ComputeMetrics(metric_instance, context)

    # main loop - where all the work is done
    for in_file in context['in_file_names']:
        try:
            cm.reset()
            fin = open(in_file, 'r')
            code = ''.join(fin.readlines())
            fin.close()
            # define lexographical scanner to use for this run
            lex = guess_lexer_for_filename(in_file, code)
            token_list = lex.get_tokens(code) # parse code

            metrics[in_file] = {}
            metrics[in_file].update(cm(token_list))
            metrics[in_file]['language'] = lex.name # provide language


        except IOError, e:
            sys.stderr.writelines(str(e) + " -- Skipping input file.\n\n")

    if context['verbose']:
        # display details
        print 'Examining %d file(s):' % len(metrics)
        display_header(context, metric_instance, '', 'File')
        display_separator(context, metric_instance, '', '-'*20)
        for in_file in metrics:
            display_metrics(context, metric_instance, '', in_file,
                metrics[in_file])
        print

    if not context['quiet']:
        # display agregated metric values on language level
        # aggregate values
        summary = {}
        for m in metrics:
            lang = metrics[m]['language']
            has_key = summary.has_key(lang)
            if not has_key:
                summary[lang] = {'file_count': 0, 'language': lang}
                #summary[lang]['file_count'] = 0
            summary[lang]['file_count'] += 1
            for i in metrics[m]:
                if i == 'language':
                    continue
                if not has_key:
                    summary[lang][i] = 0
                summary[lang][i] += metrics[m][i]

        total ={'language': 'Total'}
        for m in summary:
            for i in summary[m]:
                if i == 'language':
                    continue
                if not total.has_key(i):
                    total[i] = 0
                total[i] += summary[m][i]

        print 'Metrics Summary:'

        display_header(context, metric_instance, 'Files', '')
        display_separator(context, metric_instance, '-'*5, '')
        for m in summary:
            display_metrics(context, metric_instance, '%5d' % 
                summary[m]['file_count'], '', summary[m])
        display_separator(context, metric_instance, '-'*5, '')
        display_metrics(context, metric_instance, '%5d' % total['file_count'],
            '', total)

    return metrics


if __name__ == "__main__":
    # process command line args
    main()
