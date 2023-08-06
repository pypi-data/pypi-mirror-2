# Copyright (C) 2010-2011 Richard Lincoln
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

"""Global test counters.
"""

class TestGlobals(object):
    t_quiet = False
    t_num_of_tests = 0
    t_counter = 0
    t_ok_cnt = 0
    t_not_ok_cnt = 0
    t_skip_cnt = 0
    t_clock = 0.0
