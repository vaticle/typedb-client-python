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

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from typedb.api.connection.user import UserManager, User
# from typedb.connection.cluster.database import _FailsafeTask, _ClusterDatabase
from typedb.connection.user import _User

from typedb.typedb_client_python import user_manager_new, Connection as NativeConnection, users_contains, users_create, \
    users_delete, users_all, users_get, users_set_password, users_current_user

# if TYPE_CHECKING:
#     from typedb.connection.client import _Client

class _UserManager(UserManager):

    def __init__(self, connection: NativeConnection):
        self._user_manager = user_manager_new(connection)
        self._connection = connection

    def contains(self, username: str) -> bool:
        return users_contains(self._user_manager, username)

    def create(self, username: str, password: str) -> None:
        users_create(self._user_manager, username, password)

    def delete(self, username: str) -> None:
        users_delete(self._user_manager, username)

    def all(self) -> list[User]:
        return [_User(user, self._connection) for user in users_all(self._user_manager)]

    # def _get_user_list(self, replica: _ClusterDatabase.Replica):
    #     users_proto = self._client._stub(replica.address()).users_all(cluster_user_manager_all_req())
    #     return [_User.of(user, self._client) for user in users_proto.users]

    def get(self, username: str) -> Optional[User]:
        if user := users_get(self._user_manager, username):
            return _User(user, self._connection)
        return None

    def password_set(self, username: str, password: str) -> None:
        users_set_password(self._user_manager, username, password)

    def get_current_user(self) -> User:
        return _User(users_current_user(self._user_manager), self._connection)