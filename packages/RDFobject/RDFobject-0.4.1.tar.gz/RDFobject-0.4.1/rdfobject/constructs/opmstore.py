#!/usr/bin/env python

from rdfobject import FileMultiEntityFactory

from rdfobject.stores.storage_exceptions import *

from rdfobject.stores import StoreAlreadyExistsException,StoreNotFoundException

from uuid import uuid4

NS_OPM = "http://openprovenance.org/ontology#"

class IdentifierRequired(Exception):
  """Indicates that the trivial algorithm used to autoincrement ids has failed, likely due to non-integer ids being used in the store."""
  pass

class ActionIdentifierAlreadyExists(ObjectAlreadyExistsException):
  pass

class OPMStore(object):
  def __init__(self, store_dir="/opm_data",
                     process_prefix_uri="info:process/",
                     agent_prefix_uri="info:agent/",
                     action_prefix_uri="info:action/",
                     ):
    self._s = FileMultiEntityFactory(store_dir=store_dir)
    self.process_prefix_uri = process_prefix_uri
    self.agent_prefix_uri = agent_prefix_uri
    self.action_prefix_uri = action_prefix_uri
    self._init_substores()

  def _init_substores(self):
    # Processes
    try:
      self.process_store = self._s.get_store("processes")
    except StoreNotFoundException:
      self.process_store = self._s.add_store("processes", uri_base=self.process_prefix_uri)
    # Agents
    try:
      self.agent_store = self._s.get_store("agents")
    except StoreNotFoundException:
      self.agent_store = self._s.add_store("agents", uri_base=self.agent_prefix_uri)
    # Actions
    try:
      self.action_store = self._s.get_store("actions")
    except StoreNotFoundException:
      self.action_store = self._s.add_store("actions", uri_base=self.action_prefix_uri)

  def get_next_id(self, store):
    last_process = sorted([x for x in store.list_ids()])[-1]
    try:
      last_process_id = int(last_process)
      return last_process_id
    except ValueError:
      return # a None return signifies that this approach can't work reliably once random ids are added.

  def get_process(self, ident=None):
    if not ident:
      ident = self.get_next_id(self.process_store)
      if not ident: raise IdentiferRequired
    return self.process_store.get_id(ident)
  
  def process_exists(self, process_ident):
    return self.process_store.exists(process_ident)
  
  def list_processes(self):
    return self.process_store.list_ids()
  
  def delete_process(self, ident):
    if self.process_store.exists(ident):
      # Going to assume that you know what you are doing here
      self.process_store.delete_id(ident)
    else:
      raise ObjectNotFoundException

  def get_agent(self, ident=None):
    if not ident:
      ident = self.get_next_id(self.agent_store)
      if not ident: raise IdentiferRequired
    return self.agent_store.get_id(ident)
    
    if process_ident:
      report['process'] = process_ident
    else:
      process_ident = self.get_next_id(self.process_store)
    report[self.process_uri_base + process_ident] = "Valid"
    if not self.process_exists(process_ident):
      report[self.process_uri_base + process_ident] = "Invalid"
  def agent_exists(self, agent_ident):
    return self.agent_store.exists(agent_ident)
  
  def list_agents(self):
    return self.agent_store.list_ids()  
    
  def delete_agent(self, ident):
    if self.agent_store.exists(ident):
      # Going to assume that you know what you are doing here
      self.agent_store.delete_id(ident)
    else:
      raise ObjectNotFoundException

  def set_agent(self, agent_ident):
    if self.agent_store.exists(agent_ident):
      self.default_agent = agent_ident
      return
    else:
      raise ObjectNotFoundException

  def journal_action(self, process_ident=None, agent_ident=None, artifacts_used=[], artifacts_created=[], action_ident=None):
    if action_ident and self.action_store.exists(action_ident):
      raise ActionIdentifierAlreadyExists
    if not action_ident:
      action_ident = uuid4().hex
      while (self.action_store.exists(action_ident)):
        action_ident = uuid4().hex
    action_obj = self.action_store.get_id(action_ident)
    action_obj.add_namespace("opm", NS_OPM)
    report = {}
    if process_ident:
      report['process'] = process_ident
    else:
      process_ident = self.get_next_id(self.process_store)
    report[self.process_uri_base + process_ident] = "Valid"
    if not self.process_exists(process_ident):
      report[self.process_uri_base + process_ident] = "Invalid"
    if agent_ident:
      report['agent'] = agent_ident
    elif self.default_agent:
      report['agent'] = self.default_agent
      agent_ident = self.default_agent
    else:
      agent_ident = self.get_next_id(self.agent_store)
    report[self.agent_uri_base + agent_ident] = "Valid"
    if not self.agent_exists(agent_ident):
      report[self.agent_uri_base + agent_ident] = "Invalid"
    # Journal the action
    action_obj.add_triple(
