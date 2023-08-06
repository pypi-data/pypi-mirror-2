##############################################################################
#
# Copyright (c) 2010 Vifib SARL and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import os
import urllib
import urllib2
import pkg_resources
from slapos.lib.recipe.BaseSlapRecipe import BaseSlapRecipe

class Recipe(BaseSlapRecipe):

  def _install(self):
    self.parameter_dict = self.computer_partition.getInstanceParameterDict()
    software_type = self.parameter_dict.get('slap_software_type', 'kumo_cloud')
    if software_type is None:
      software_type = 'kumo_cloud'
    if "run_%s" % software_type in dir(self) and \
       callable(getattr(self, "run_%s" % software_type)):
      return getattr(self, "run_%s" % software_type)()
    else:
      raise NotImplementedError("Do not support %s" % software_type)

  def run_kumo_cloud(self):
    """ """

    kumo_cloud_config = {}
    kumo_cloud_config.update(self.options)

    kumo_cloud_config['address'] = self.getGlobalIPv6Address()

    kumo_cloud_config['report_path'] = self.log_directory
    kumo_cloud_config['software_release_url'] = self.software_release_url
    kumo_cloud_config['server_url'] = self.server_url
    kumo_cloud_config['key_file'] = self.key_file
    kumo_cloud_config['cert_file'] = self.cert_file
    kumo_cloud_config['computer_id'] = self.computer_id
    kumo_cloud_config['computer_partition_id'] = self.computer_partition_id

    nosqltester_manager_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'nosqltester_manager_run.in'))
    nosqltester_manager_runner_path = self.createRunningWrapper("nosqltester_manager",
          self.substituteTemplate(nosqltester_manager_wrapper_template_location, kumo_cloud_config))

    return [nosqltester_manager_runner_path]

  def run_all(self):
    """ Runs all services on one machine. """
    all_config = {}
    all_config.update(self.options)

    ipaddress = "[%s]" % self.getGlobalIPv6Address()

    all_config['manager_address'] = ipaddress
    all_config['manager_port'] = 19700
    all_config['server_address'] = ipaddress
    all_config['server_port'] = 19800
    all_config['server_listen_port'] = 19900
    all_config['server_storage'] = os.path.join(self.data_root_directory, "kumodb.tch")
    all_config['gateway_address'] = ipaddress
    all_config['gateway_port'] = 11411
    all_config['manager_log'] = os.path.join(self.log_directory, "kumo-manager.log")
    all_config['server_log'] = os.path.join(self.log_directory, "kumo-server.log")
    all_config['gateway_log'] = os.path.join(self.log_directory, "kumo-gateway.log")

    manager_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'kumo_manager_run.in'))
    manager_runner_path = self.createRunningWrapper("kumo-manager",
          self.substituteTemplate(manager_wrapper_template_location, all_config))
    server_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'kumo_server_run.in'))
    server_runner_path = self.createRunningWrapper("kumo-server",
          self.substituteTemplate(server_wrapper_template_location, all_config))
    gateway_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'kumo_gateway_run.in'))
    gateway_runner_path = self.createRunningWrapper("kumo-gateway",
          self.substituteTemplate(gateway_wrapper_template_location, all_config))

    return [manager_runner_path, server_runner_path, gateway_runner_path]

  def run_kumo_manager(self, ipaddress=None):
    """ Runs the kumofs manager. """
    manager_config = {}
    manager_config.update(self.options)

    if ipaddress is None:
      manager_config['manager_address'] = "[%s]" % self.getGlobalIPv6Address()
    else:
      manager_config['manager_address'] = ipaddress
    
    manager_config['manager_port'] = 19700
    manager_config['manager_log'] = os.path.join(self.log_directory, "kumo-manager.log")

    self.computer_partition.setConnectionDict(manager_config)

    manager_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'kumo_manager_run.in'))
    manager_runner_path = self.createRunningWrapper("kumo-manager",
          self.substituteTemplate(manager_wrapper_template_location, manager_config))

    return [manager_runner_path]

  def run_kumo_server(self):
    """ Runs the kumofs server. """
    server_config = {}
    server_config.update(self.options)
    server_config.update(self.parameter_dict)

    server_config['server_address'] = "[%s]" % self.getGlobalIPv6Address()
    server_config['server_port'] = 19800
    server_config['server_listen_port'] = 19900
    server_config['server_storage'] = os.path.join(self.var_directory,"kumodb.tch")
    server_config['server_log'] = os.path.join(self.log_directory, "kumo-server.log")

    self.computer_partition.setConnectionDict(server_config)

    server_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'kumo_server_run.in'))
    server_runner_path = self.createRunningWrapper("kumo-server",
          self.substituteTemplate(server_wrapper_template_location, server_config))

    return [server_runner_path]

  def run_kumo_gateway(self):
    """ Runs the kumofs gateway. """
    gateway_config = {}
    gateway_config.update(self.options)
    gateway_config.update(self.parameter_dict)

    gateway_config['gateway_address'] = "[%s]" % self.getGlobalIPv6Address()
    gateway_config['gateway_port'] = 11411
    gateway_config['gateway_log'] = os.path.join(self.log_directory, "kumo-gateway.log")

    self.computer_partition.setConnectionDict(gateway_config)

    gateway_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'kumo_gateway_run.in'))
    gateway_runner_path = self.createRunningWrapper("kumo-gateway",
          self.substituteTemplate(gateway_wrapper_template_location, gateway_config))

    return [gateway_runner_path]

  def run_nosqltester(self):
    """ Runs the kumofs tester. """
    tester_config = {}
    tester_config.update(self.options)
    tester_config.update(self.parameter_dict)

    tester_config['tester_address'] = self.getGlobalIPv6Address()
    tester_config['url'] = "http://%s:5000/" % tester_config['tester_address']
    tester_config['start_url'] = "http://%s:5000/start" % tester_config['tester_address']
    tester_config['report_path'] = self.log_directory

    self.computer_partition.setConnectionDict(tester_config)

    tester_wrapper_template_location = pkg_resources.resource_filename(
                                             __name__, os.path.join(
                                             'template', 'nosqltester_run.in'))
    tester_runner_path = self.createRunningWrapper("nosqltester",
          self.substituteTemplate(tester_wrapper_template_location, tester_config))

    return [tester_runner_path]

