# (C) Copyright 2008 Nuxeo SAS <http://nuxeo.com>
# Author: bdelbosc@nuxeo.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
"""Choose the best html rendering

$Id: ReportRenderHtml.py 54287 2011-02-04 23:40:50Z bdelbosc $
"""

try:
    # 1/ gnuplot
    from ReportRenderHtmlGnuPlot import RenderHtmlGnuPlot as RenderHtml
except ImportError:
    try:
        # 2/ gdchart2
        from ReportRenderHtmlGDChart import RenderHtmlGDChart as RenderHtml
        import warnings
        warnings.warn('GDChart library is deprecated and will be removed '
                      'in 1.15, FunkLoad is now using gnuplot > 4.2')
    except:
        # 3/ no charts
        from ReportRenderHtmlBase import RenderHtmlBase as RenderHtml

from ReportRenderHtmlGnuPlot import RenderHtmlGnuPlot as RenderHtml
