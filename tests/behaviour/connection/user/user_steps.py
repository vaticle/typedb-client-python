#
#   Copyright (C) 2022 Vaticle
#
#   Licensed to the Apache Software Foundation (ASF) under one
#   or more contributor license agreements.  See the NOTICE file
#   distributed with this work for additional information
#   regarding copyright ownership.  The ASF licenses this file
#   to you under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in compliance
#   with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing,
#   software distributed under the License is distributed on an
#   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#   KIND, either express or implied.  See the License for the
#   specific language governing permissions and limitations
#   under the License.
#
import os

from behave import step
from hamcrest import assert_that, has_item, not_
from typedb.client import *

from tests.behaviour.context import Context


def _get_client(context: Context):
    client = context.client
    assert isinstance(client, TypeDBClusterClient)
    return client


@step("users contains: {username}")
def step_impl(context: Context, username: str):
    assert_that([u.username() for u in _get_client(context).users().all()], has_item(username))


@step("users not contains: {username}")
def step_impl(context: Context, username: str):
    assert_that([u.username() for u in _get_client(context).users().all()], not_(has_item(username)))


@step("users create: {username:w}, {password:w}")
def step_impl(context: Context, username: str, password: str):
    _get_client(context).users().create(username, password)



@step("users create: {username:w}, {password:w}; throws exception")
def step_impl(context: Context, username: str, password: str):
    try :
        _get_client(context).users().create(username, password)
        assert False
    except TypeDBClientException:
        pass


@step("users get all")
def step_impl(context: Context):
    _get_client(context).users().all()


@step("users get all; throws exception")
def step_impl(context: Context):
    try:
        _get_client(context).users().all()
        assert False
    except TypeDBClientException:
        pass


@step("users get user: {username:w}")
def step_impl(context: Context, username: str):
    _get_client(context).users().get(username)


@step("users get user: {username:w}; throws exception")
def step_impl(context: Context, username: str):
    try :
        _get_client(context).users().get(username)
        assert False
    except TypeDBClientException:
        pass


@step("users delete: {username}")
def step_impl(context: Context, username: str):
    _get_client(context).users().delete(username)


@step("users password set: {username}, {password}")
def step_impl(context: Context, username: str, password: str):
    _get_client(context).users().password_set(username, password)


@step("users password update: {username}, {password_old}, {password_new}")
def step_impl(context: Context, username: str, password_old: str, password_new: str):
    _get_client(context).users().get(username).password_update(password_old, password_new)
