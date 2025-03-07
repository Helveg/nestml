# -*- coding: utf-8 -*-
#
# nest_custom_templates_test.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.
import os
import unittest

import nest

from pynestml.frontend.pynestml_frontend import to_nest
from pynestml.utils.model_installer import install_nest


class NestCustomTemplatesTest(unittest.TestCase):
    """
    Tests the code generation and installation with custom NESTML templates for NEST
    """

    def test_custom_templates(self):
        input_path = os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.join(
            os.pardir, os.pardir, "models", "iaf_psc_exp.nestml"))))
        nest_path = nest.ll_api.sli_func("statusdict/prefix ::")
        target_path = 'target'
        logging_level = 'INFO'
        module_name = 'nestmlmodule'
        store_log = False
        suffix = '_nestml'
        dev = True

        codegen_opts = {"templates": {
            "path": 'point_neuron',
            "model_templates": ['NeuronClass.cpp.jinja2', 'NeuronHeader.h.jinja2'],
            "module_templates": ['setup/CMakeLists.txt.jinja2',
                                 'setup/ModuleHeader.h.jinja2', 'setup/ModuleClass.cpp.jinja2']
        }}

        to_nest(input_path, target_path, logging_level, module_name, store_log, suffix, dev, codegen_opts)
        install_nest(target_path, nest_path)
        nest.set_verbosity("M_ALL")

        nest.ResetKernel()
        nest.Install("nestmlmodule")

        nrn = nest.Create("iaf_psc_exp_nestml")
        mm = nest.Create('multimeter')
        mm.set({"record_from": ["V_m"]})

        nest.Connect(mm, nrn)

        nest.Simulate(5.0)
