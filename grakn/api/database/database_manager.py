#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from abc import ABC, abstractmethod
from typing import List

from grakn.api.database.database import Database, DatabaseCluster


class DatabaseManager(ABC):

    @abstractmethod
    def contains(self, name: str) -> bool:
        pass

    @abstractmethod
    def create(self, name: str) -> None:
        pass

    @abstractmethod
    def get(self, name: str) -> Database:
        pass

    @abstractmethod
    def all(self) -> List[Database]:
        pass


class DatabaseManagerCluster(DatabaseManager, ABC):

    @abstractmethod
    def get(self, name: str) -> DatabaseCluster:
        pass

    @abstractmethod
    def all(self) -> List[DatabaseCluster]:
        pass
