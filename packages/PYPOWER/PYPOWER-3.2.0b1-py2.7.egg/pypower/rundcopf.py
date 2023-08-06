# Copyright (C) 1996-2011 Power System Engineering Research Center
# Copyright (C) 2009-2011 Richard Lincoln
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Runs a DC optimal power flow.
"""

from os.path import dirname, join

from pypower.ppoption import ppoption
from pypower.runopf import runopf


def rundcopf(casedata=None, ppopt=None, fname='', solvedcase=''):
    """Runs a DC optimal power flow.

    @author: Ray Zimmerman (PSERC Cornell)
    @author: Richard Lincoln
    """
    ## default arguments
    if casedata is None:
        casedata = join(dirname(__file__), 'case9')
    ppopt = ppoption(ppopt, PF_DC=True)

    return runopf(casedata, ppopt, fname, solvedcase)


if __name__ == '__main__':
    rundcopf()