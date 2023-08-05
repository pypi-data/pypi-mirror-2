#!/usr/bin/python

# Copyright (c) 2009, Purdue University
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
# 
# Neither the name of the Purdue University nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Core helper functions."""

__copyright__ = 'Copyright (C) 2009, Purdue University'
__license__ = 'BSD'
__version__ = '0.14'


import constants
import core
import errors
import helpers_lib
import user

import datetime
import math

import IPy

class RecordsBatchError(errors.CoreError):
  pass

class CoreHelpers(object):
  """Library of helper functions that extend the core functions."""
  def __init__(self, core_instance):
    """Sets up core instance

    Inputs:
       core_instance: instance of RosterCore
    """
    self.core_instance = core_instance
    self.db_instance = core_instance.db_instance
    self.user_instance = core_instance.user_instance
    self.log_instance = core_instance.log_instance

  ### These functions just expose helpers_lib functions for the 
  ### XML-RPC server. For doc strings see helpers_lib
  def ListAccessRights(self):
    return helpers_lib.ListAccessRights()

  def ReverseIP(self, ip_address):
    return helpers_lib.ReverseIP(ip_address)

  def UnReverseIP(self, ip_address):
    return helpers_lib.UnReverseIP(ip_address)

  def CIDRExpand(self, cidr_block):
    return helpers_lib.CIDRExpand(cidr_block)

  def ExpandIPV6(self, ip_address):
    return helpers_lib.ExpandIPV6(ip_address)

  def ListLatestNamedConfig(self, dns_server_set):
    """Lists the latest named config string given dns server set

    This function is duplicated in
    roster-config-manager/roster_config_manager/tree_exporter.py

    Inputs:
      dns_server_set: string of dns server set name

    Outputs:
      dict: dictionary of latest named config
    """
    named_configs = self.core_instance.ListNamedConfGlobalOptions(
        dns_server_set=dns_server_set)
    current_timestamp = datetime.datetime.now()
    smallest_time_differential = datetime.timedelta(weeks=100000)
    newest_config = None
    for named_config in named_configs:
      time_differential = current_timestamp - named_config['timestamp']
      if( time_differential < smallest_time_differential ):
        smallest_time_differential = time_differential
        newest_config = named_config

    return newest_config

  def RevertNamedConfig(self, dns_server_set, option_id):
    """Revert a Named Config file

    Inputs:
      option_id: the id of config to replicate
      dns_server_set: string of dns server set name
    """
    named_config = self.core_instance.ListNamedConfGlobalOptions(
        dns_server_set=dns_server_set, option_id=option_id)
    if( len(named_config) == 0 ):
      raise errors.CoreError('DNS server set "%s" does not contain id "%s"' % (
          dns_server_set, option_id))
    elif( len(named_config) == 1 ):
      self.core_instance.MakeNamedConfGlobalOption(
          dns_server_set, named_config[0]['options'])
    else:
      raise errors.CoreError('Multiple configurations found.')

  def MakeAAAARecord(self, target, zone_name, record_args_dict,
                     view_name=None, ttl=None):
    """Makes an AAAA record.

    Inputs:
      target: string of target
      zone_name: string of zone name
      record_args_dict: dictionary of record arguments
      view_name: string of view name
      ttl: time to live
    """
    record_args_dict['assignment_ip'] = unicode(IPy.IP(record_args_dict[
        'assignment_ip']).strFullsize())
    self.core_instance.MakeRecord(u'aaaa', target, zone_name, record_args_dict,
                                  view_name, ttl)

  def GetPTRTarget(self, long_target, view_name=u'any'):
    """Gets the short PTR target given the long PTR target

    Inputs:
      long_target: String of long PTR target
      view_name: String of view name

    Ouptuts:
      string: String of short PTR target
    """
    if( not long_target.endswith('in-addr.arpa.') and not
        long_target.endswith('ip6.arpa.') ):
      long_target = self.ReverseIP(long_target)
    zone_assignment = None
    reverse_range_zone_assignments = (
        self.core_instance.ListReverseRangeZoneAssignments())
    ip_address = IPy.IP(self.UnReverseIP(long_target))
    for zone_assignment in reverse_range_zone_assignments:
      if( zone_assignment in reverse_range_zone_assignments ):
        if( ip_address in IPy.IP(
            reverse_range_zone_assignments[zone_assignment]) ):
          break
    else:
      raise errors.CoreError(
          'No suitable reverse range zone assignments found.')
    zone_detail = self.core_instance.ListZones(view_name=view_name)
    zone_origin = zone_detail[zone_assignment][view_name]['zone_origin']
    # Count number of characters in zone origin, add one to count the extra
    # period and remove that number of characters from the target.
    zone_origin_length = len(zone_origin) + 1
    short_target = long_target[:-zone_origin_length:]

    return (short_target, zone_assignment)

  def MakePTRRecord(self, target, record_args_dict,
                    view_name=u'any', ttl=None):
    """Makes a ptr record.

    Inputs:
      target: string of target
      record_args_dict: dictionary of record arguments
      view_name: string of view name
      ttl: string of ttl
    """
    target, zone_assignment = self.GetPTRTarget(target, view_name)
    if( record_args_dict['assignment_host'].startswith('@.') ):
      record_args_dict['assignment_host'] = record_args_dict[
          'assignment_host'].lstrip('@.')
    self.core_instance.MakeRecord(u'ptr', target, zone_assignment,
                                  record_args_dict, view_name, ttl)

  def RemovePTRRecord(self, record_type, target, zone_name, record_args_dict,
                      view_name, ttl=None):
    """Removes a ptr record.

    Inputs:
      target: string of target
      record_args_dict: dictionary of record arguments
      view_name: string of view name
      ttl: string of ttl
    """
    if( record_args_dict['assignment_host'].startswith('@.') ):
      record_args_dict['assignment_host'] = record_args_dict[
          'assignment_host'].lstrip('@.')
    self.core_instance.RemoveRecord(u'ptr', target, zone_name,
                                    record_args_dict, view_name, ttl)

  def ListRecordsByCIDRBlock(self, cidr_block, view_name=None, zone_name=None):
    """Lists records in user given cidr block.

    Inputs:
      cidr_block: string of ipv4 or ipv6 cidr block

    Outputs:
      dict: dictionary keyed by ip address example:
            {u'192.168.1.7': {u'a': False, u'host': u'host5.',
                              u'ptr': True, u'zone': u'test_zone',
                              u'view': u'test_view2'},
             u'192.168.1.5': {u'a': True, u'host': u'host3.',
             u'ptr': True, u'zone': u'test_zone', u'view': u'test_view2'}}
    """
    user_cidr = IPy.IP(cidr_block)
    record_type = u'a'
    if( user_cidr.version() == 6 ):
      record_type = u'aaaa'
    zones = self.core_instance.ListZones()

    ptr_record_list = []
    fwd_record_list = []
    zone_list = []

    ptr_dict = self.db_instance.GetEmptyRowDict('records')
    ptr_dict['record_type'] = u'ptr'
    ptr_args_dict = self.db_instance.GetEmptyRowDict(
        'record_arguments_records_assignments')

    zone_dict = self.db_instance.GetEmptyRowDict(
        'reverse_range_zone_assignments')

    fwd_dict = self.db_instance.GetEmptyRowDict('records')
    fwd_dict['record_type'] = record_type
    if( view_name is not None and view_name.endswith('_dep')
        or view_name == u'any' ):
      fwd_dict['record_view_dependency'] = view_name
      ptr_dict['record_view_dependency'] = view_name
    elif( view_name is not None ):
      fwd_dict['record_view_dependency'] = '%s_dep' % view_name
      ptr_dict['record_view_dependency'] = '%s_dep' % view_name
    fwd_args_dict = self.db_instance.GetEmptyRowDict(
        'record_arguments_records_assignments')
    fwd_args_dict['record_arguments_records_assignments_argument_name'] = (
        u'assignment_ip')
    self.db_instance.StartTransaction()
    try:
      reverse_range_zone_assignments_db = (
          self.db_instance.ListRow(
              'reverse_range_zone_assignments', zone_dict))
      for reverse_range_zone_assignment in reverse_range_zone_assignments_db:
        db_zone = reverse_range_zone_assignment[
            'reverse_range_zone_assignments_zone_name']
        db_cidr = IPy.IP(reverse_range_zone_assignment[
            'reverse_range_zone_assignments_cidr_block'])
        if( user_cidr in db_cidr ):
          zone_list = [db_zone]
          break
        if( db_cidr in user_cidr ):
          zone_list.append(db_zone)
      for zone in zone_list:
        ptr_dict['record_zone_name'] = zone
        ptr_record_list.extend(self.db_instance.ListRow(
            'records', ptr_dict, 'record_arguments_records_assignments',
            ptr_args_dict))
      num_records = self.db_instance.TableRowCount('records')
      ratio = num_records / float(user_cidr.len())
      if( ratio > constants.RECORD_RATIO ):
        for ip_address in user_cidr:
          fwd_args_dict['argument_value'] = unicode(ip_address.strFullsize())
          fwd_record_list.extend(self.db_instance.ListRow(
              'records', fwd_dict, 'record_arguments_records_assignments',
              fwd_args_dict))
      else:
        fwd_record_list = self.db_instance.ListRow('records',
            fwd_dict, 'record_arguments_records_assignments', fwd_args_dict)
    finally:
      self.db_instance.EndTransaction()
    records_dict = {}
    orig_view = view_name
    for record in ptr_record_list:
      view_name = orig_view
      record_zone_name = record['record_zone_name']
      db_view_name = record['record_view_dependency'].rsplit('_dep', 1)[0]
      if( db_view_name != view_name and (db_view_name != u'any' and view_name is not None) ):
        continue
      if( zone_name and record_zone_name != zone_name ):
        continue
      if( view_name is None ):
        view_name = db_view_name
      if( db_view_name not in zones[record_zone_name]  ):
        raise errors.CoreError('No zone view combination found for '
                               '"%s" zone and "%s" view.' % (
                                   record_zone_name, db_view_name))
      zone_origin = zones[record_zone_name][db_view_name]['zone_origin']
      reverse_ip_address = '%s.%s' % (record['record_target'], zone_origin)
      ip_address = self.UnReverseIP(reverse_ip_address)
      if( IPy.IP(ip_address) in user_cidr ):
        if( not db_view_name in records_dict ):
          records_dict[db_view_name] = {}
        if( not ip_address in records_dict[db_view_name] ):
          records_dict[db_view_name][ip_address] = []
        records_dict[db_view_name][ip_address].append({
            u'forward': False, u'host': record['argument_value'].rstrip('.'),
            u'zone': record['record_zone_name'], 'zone_origin': zone_origin})
    for record in fwd_record_list:
      view_name = orig_view
      ip_address = record['argument_value']
      record_zone_name = record['record_zone_name']
      db_view_name = record['record_view_dependency'].rsplit('_dep', 1)[0]
      if( db_view_name != view_name and (db_view_name != u'any' and view_name is not None) ):
        continue
      if( zone_name and record_zone_name != zone_name ):
        continue
      if( view_name is None ):
        view_name = db_view_name
      zone_origin = zones[record_zone_name][db_view_name]['zone_origin']
      if( IPy.IP(ip_address) in user_cidr ):
        if( not db_view_name in records_dict ):
          records_dict[db_view_name] = {}
        if( not ip_address in records_dict[db_view_name] ):
           records_dict[db_view_name][ip_address] = []
        records_dict[db_view_name][ip_address].append({
            u'forward': True, u'host': '%s.%s' % (
                record['record_target'], zone_origin.rstrip('.')),
            u'zone': record['record_zone_name'],
            u'zone_origin': zone_origin})
    return records_dict

  def ListNamedConfGlobalOptionsClient(self, option_id=None,
                                       dns_server_set=None, timestamp=None):
    """Converts XMLRPC datetime to datetime object and runs
    ListNamedConfGlobalOptions

    Inputs:
      option_id: integer of the option id
      dns_server_set: string of the dns server set name
      timestamp: XMLRPC datetime timestamp

    Outputs:
      list: list of dictionarires from ListNamedConfGlobalOptions
    """
    return self.core_instance.ListNamedConfGlobalOptions(
        option_id, dns_server_set, timestamp)

  def ListZoneByIPAddress(self, ip_address):
    """Lists zone name given ip_address

    Inputs:
      ip_address: string of ip address

    Outputs:
      string: string of zone name, ex: 'test_zone'
    """
    user_ip = IPy.IP(ip_address)
    reverse_range_zone_assignments = (
        self.core_instance.ListReverseRangeZoneAssignments())
    for reverse_range_zone_assignment in reverse_range_zone_assignments:
      db_cidr = IPy.IP(reverse_range_zone_assignments[
          reverse_range_zone_assignment])
      if( user_ip in db_cidr ):
        return reverse_range_zone_assignment

  def RemoveCNamesByAssignmentHost(self, hostname, view_name, zone_name):
    """Removes cname's by assignment hostname, will not remove cnames
    that the user does not have permissin to remove. The function will continue
    and pass over that cname.

    Inputs:
      hostname: string of hostname
      view_name: string of view name
      zone_name: string of zone name

    Outputs:
      int: number of rows modified
    """
    function_name, current_args = helpers_lib.GetFunctionNameAndArgs()

    record_arguments_record_assignments_dict = (
        self.db_instance.GetEmptyRowDict(
            'record_arguments_records_assignments'))
    record_arguments_record_assignments_dict[
        'record_arguments_records_assignments_type'] = u'cname'
    record_arguments_record_assignments_dict[
        'argument_value'] = hostname
    records_dict = self.db_instance.GetEmptyRowDict(
        'records')
    records_dict['record_type'] = u'cname'
    records_dict['record_view_dependency'] = '%s_dep' % view_name
    records_dict['record_zone_name'] = zone_name
    success = False
    try:
      self.db_instance.StartTransaction()
      try:
        found_record_arguments = self.db_instance.ListRow(
            'record_arguments_records_assignments',
            record_arguments_record_assignments_dict)
        remove_record_dict = {}
        for record_argument in found_record_arguments:
          remove_record_dict[record_argument[
              'record_arguments_records_assignments_record_id']] = {
                  'assignment_host': record_argument['argument_value']}
        row_count = 0
        for record_id in remove_record_dict:
          records_dict['records_id'] = record_id
          found_records_dict = self.db_instance.ListRow(
              'records', records_dict)
          if( len(found_records_dict) != 1 ):
            raise errors.CoreError('Incorrect number of records found!')
          try:
            self.core_instance.user_instance.Authorize(
                'RemoveRecord',
                 record_data=
                     {'target': records_dict['record_target'],
                      'zone_name': records_dict['record_zone_name'],
                      'view_name': records_dict['record_view_dependency']},
                current_transaction=True)
          except user.AuthError:
            continue
          row_count += self.db_instance.RemoveRow(
              'records', found_records_dict[0])
          remove_record_dict[record_id].update({
              'cname_host': found_records_dict[0]['record_target']})
      except:
        self.db_instance.EndTransaction(rollback=True)
        raise
      self.db_instance.EndTransaction()
      success = True
      remove_record_string = ''
      log_list = []
      for record_id in remove_record_dict:
        log_list.append('record_id:')
        log_list.append(str(record_id))
        for record in remove_record_dict[record_id]:
          log_list.append('%s:' % record)
          log_list.append(remove_record_dict[record_id][record])
      if( log_list ):
        remove_record_string = ' '.join(log_list)
    finally:
      self.log_instance.LogAction(self.user_instance.user_name, function_name,
                                  current_args, success)
    return row_count

  def ProcessRecordsBatch(self, delete_records=[], add_records=[]):
    """Proccess batches of records

    Inputs:
      delete_records: list of dictionaries of records
                      ex: {'record_type': 'a', 'record_target': 'target',
                           'view_name': 'view', 'zone_name': 'zone',
                           'record_arguments': {'assignment_ip': '1.2.3.4'}}
      add_records: list of dictionaries of records

    Outputs:
      int: row count
    """
    function_name, current_args = helpers_lib.GetFunctionNameAndArgs()

    log_dict = {'delete': [], 'add': []}
    row_count = 0
    changed_view_dep = []
    success = False
    try:
      self.db_instance.StartTransaction()
      try:
        # REMOVE RECORDS
        for record in delete_records:
          records_dict = self.db_instance.GetEmptyRowDict('records')
          records_dict['record_type'] = record['record_type']
          records_dict['record_target'] = record['record_target']
          records_dict['record_zone_name'] = record['record_zone_name']
          view_name = record['view_name']
          if( not record['view_name'].endswith('_dep') and record[
                'view_name'] != u'any'):
            view_name = '%s_dep' % record['view_name']
          changed_view_dep.append((view_name, record['record_zone_name']))
          records_dict['record_view_dependency'] = view_name
          self.user_instance.Authorize('RemoveRecord',
              record_data =
                  {'target': record['record_target'],
                   'zone_name': record['record_zone_name'],
                   'view_name': records_dict['record_view_dependency']},
              current_transaction=True)

          if( 'record_ttl' in record ):
            records_dict['record_ttl'] = record['record_ttl']
          args_list = []
          for argument in record['record_arguments']:
            if( record['record_arguments'][argument] is None ):
              raise errors.CoreErrore('%s: "%s" cannot be None' % (
                  record['record_target'], argument))
            args_list.append(
                {u'record_arguments_records_assignments_argument_name':
                     argument,
                 u'record_arguments_records_assignments_type':
                     record['record_type'],
                 u'argument_value': record['record_arguments'][argument],
                 u'record_arguments_records_assignments_record_id': None})
          args_search_list = []
          record_ids = []
          final_id = []
          record_id_dict = {}
          for arg in args_list:
            args_search_list.append(self.db_instance.ListRow(
                'record_arguments_records_assignments', arg))
          for index, record_args in enumerate(args_search_list):
            record_ids.append([])
            for args_dict in record_args:
              record_ids[index].append(args_dict[
                  u'record_arguments_records_assignments_record_id'])
          for id_list in record_ids:
            for search_id in id_list:
              if( search_id in record_id_dict ):
                record_id_dict[search_id] += 1
              else:
                record_id_dict[search_id] = 1
          for record_id in record_id_dict:
            if( record_id_dict[record_id] == len(args_list) ):
              final_id.append(record_id)
          if( len(final_id) == 1 ):
            records_dict['records_id'] = final_id[0]
            new_records = self.db_instance.ListRow('records', records_dict)
            rows_deleted = self.db_instance.RemoveRow('records', new_records[0])
            if( not rows_deleted ):
              raise RecordsBatchError(
                  '%s: Record not found' % record['record_target'])
            log_dict['delete'].append(record)
            row_count += 1

        # ADD RECORDS
        for record in add_records:
          view_name = record['view_name']
          if( not record['view_name'].endswith('_dep') and record[
                'view_name'] != u'any'):
            view_name = '%s_dep' % record['view_name']
          self.user_instance.Authorize('MakeRecord', 
              record_data = {
                  'target': record['record_target'],
                  'zone_name': record['record_zone_name'],
                  'view_name': view_name},
              current_transaction=True)
          if( record['record_type'] == u'ptr' ):
            if( record['record_arguments'][
                'assignment_host'].startswith('@.') ):
              record['record_arguments']['assignment_host'] = record[
                  'record_arguments']['assignment_host'].lstrip('@.')
          changed_view_dep.append((view_name, record['record_zone_name']))
          ttl = None
          if( 'ttl' in record ):
            ttl = record['ttl']
          if( ttl is None ):
            ttl = constants.DEFAULT_TTL

          records_dict = {'records_id': None,
                          'record_target': record['record_target'],
                          'record_type': None,
                          'record_ttl': None,
                          'record_zone_name': record['record_zone_name'],
                          'record_view_dependency': view_name,
                          'record_last_user': None}

          if( record['record_type'] == 'cname' ):
            all_records = self.db_instance.ListRow('records', records_dict)
            if( len(all_records) > 0 ):
              raise RecordsBatchError(
                  'Record already exists with target %s.' % (
                      record['record_target']))
          records_dict['record_type'] = u'cname'
          cname_records = self.db_instance.ListRow('records', records_dict)
          if( len(cname_records) > 0 ):
            raise RecordsBatchError('CNAME already exists with target %s.' % (
                record['record_target']))

          record_args_assignment_dict = self.db_instance.GetEmptyRowDict(
              'record_arguments_records_assignments')
          records_dict['record_type'] = record['record_type']
          raw_records = self.db_instance.ListRow(
              'records', records_dict, 'record_arguments_records_assignments',
              record_args_assignment_dict)
          records_dict['record_last_user'] = self.user_instance.GetUserName()
          records_dict['record_ttl'] = ttl
          current_records = (
              helpers_lib.GetRecordsFromRecordRowsAndArgumentRows(
              raw_records, record['record_arguments']))
          for current_record in current_records:
            for arg in record['record_arguments'].keys():
              if( arg not in current_record ):
                break
              if( record['record_arguments'][arg] is None ):
                continue
              if( record['record_arguments'][arg] != current_record[arg] ):
                break
            else:
              raise RecordsBatchError('Duplicate record found')


          records_dict['record_type'] = record['record_type']
          record_id = self.db_instance.MakeRow('records', records_dict)
          for arg in record['record_arguments'].keys():
            record_argument_assignments_dict = {
               'record_arguments_records_assignments_record_id': record_id,
               'record_arguments_records_assignments_type': record[
                   'record_type'],
               'record_arguments_records_assignments_argument_name': arg,
               'argument_value': unicode(record['record_arguments'][arg])}
            self.db_instance.MakeRow('record_arguments_records_assignments',
                                     record_argument_assignments_dict)
            log_dict['add'].append(record)
            row_count += 1

        changed_view_dep = set(changed_view_dep)
        for view_dep_pair in changed_view_dep:
          self.core_instance._IncrementSoa(*view_dep_pair)

      except:
        self.db_instance.EndTransaction(rollback=True)
        raise
      self.db_instance.EndTransaction()
      success = True
    finally:
      self.log_instance.LogAction(self.user_instance.user_name, function_name,
                                  current_args, success)
    return row_count

# vi: set ai aw sw=2:
