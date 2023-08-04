#
# Copyright (C) 2022 Vaticle
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

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterator, Optional

from typedb.api.concept.type.type import Type
from typedb.common.transitivity import Transitivity

if TYPE_CHECKING:
    from typedb.api.concept.type.annotation import Annotation
    from typedb.api.concept.thing.thing import Thing
    from typedb.api.concept.type.role_type import RoleType
    from typedb.api.concept.value.value import ValueType
    from typedb.api.concept.type.attribute_type import AttributeType
    from typedb.api.connection.transaction import Transaction


class ThingType(Type, ABC):

    def is_thing_type(self) -> bool:
        return True

    @abstractmethod
    def get_supertype(self, transaction: Transaction) -> Optional[ThingType]:
        pass

    @abstractmethod
    def get_supertypes(self, transaction: Transaction) -> Iterator[ThingType]:
        pass

    @abstractmethod
    def get_subtypes(self, transaction: Transaction) -> Iterator[ThingType]:
        pass

    @abstractmethod
    def get_subtypes_explicit(self, transaction: Transaction) -> Iterator[ThingType]:
        pass

    @abstractmethod
    def get_instances(self, transaction: Transaction) -> Iterator[Thing]:
        pass

    @abstractmethod
    def get_instances_explicit(self, transaction: Transaction) -> Iterator[Thing]:
        pass

    @abstractmethod
    def set_abstract(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def unset_abstract(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def set_plays(self, transaction: Transaction, role_type: RoleType,
                  overriden_type: Optional[RoleType] = None) -> None:
        pass

    @abstractmethod
    def unset_plays(self, transaction: Transaction, role_type: RoleType) -> None:
        pass

    @abstractmethod
    def set_owns(self, transaction: Transaction, attribute_type: AttributeType,
                 overridden_type: Optional[AttributeType] = None,
                 annotations: Optional[set[Annotation]] = None) -> None:
        pass

    @abstractmethod
    def get_owns(self, transaction: Transaction, value_type: Optional[ValueType] = None,
                 transitivity: Transitivity = Transitivity.TRANSITIVE, annotations: Optional[set[Annotation]] = None
                 ) -> Iterator[AttributeType]:
        pass

    @abstractmethod
    def get_owns_explicit(self, transaction: Transaction, value_type: Optional[ValueType] = None,
                          annotations: Optional[set[Annotation]] = None):
        pass

    @abstractmethod
    def get_plays(self, transaction: Transaction, transitivity: Transitivity = Transitivity.TRANSITIVE) -> Iterator[RoleType]:
        pass

    @abstractmethod
    def get_plays_explicit(self, transaction: Transaction) -> Iterator[RoleType]:
        pass

    @abstractmethod
    def get_plays_overridden(self, transaction: Transaction, role_type: RoleType) -> Optional[RoleType]:
        pass

    @abstractmethod
    def unset_owns(self, transaction: Transaction, attribute_type: AttributeType) -> None:
        pass

    @abstractmethod
    def get_syntax(self, transaction: Transaction) -> str:
        pass
